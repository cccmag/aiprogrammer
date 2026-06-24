#!/usr/bin/env node

class Router {
  constructor() {
    this.routes = [];
    this.middleware = [];
  }

  use(fn) {
    this.middleware.push(fn);
  }

  get(path, ...handlers) {
    this.routes.push({ method: 'GET', path, handlers });
  }

  post(path, ...handlers) {
    this.routes.push({ method: 'POST', path, handlers });
  }

  match(method, path) {
    const segments = path.split('/').filter(Boolean);
    for (const route of this.routes) {
      if (route.method !== method) continue;
      const routeSegs = route.path.split('/').filter(Boolean);
      if (routeSegs.length !== segments.length) continue;
      const params = {};
      let ok = true;
      for (let i = 0; i < routeSegs.length; i++) {
        if (routeSegs[i].startsWith(':')) {
          params[routeSegs[i].slice(1)] = segments[i];
        } else if (routeSegs[i] !== segments[i]) {
          ok = false;
          break;
        }
      }
      if (ok) return { handlers: route.handlers, params };
    }
    return null;
  }

  async dispatch(req) {
    req.params = {};
    const ctx = { req, res: null, body: null, status: 200 };
    let idx = 0;
    let nextCalled = true;
    const run = async (i) => {
      if (i < this.middleware.length && nextCalled) {
        nextCalled = false;
        await this.middleware[i](ctx, () => { nextCalled = true; run(i + 1); });
      }
    };
    await run(0);
    if (!nextCalled) return ctx;

    const match = this.match(ctx.req.method, ctx.req.path);
    if (!match) {
      ctx.status = 404;
      ctx.body = { error: 'Not Found' };
      return ctx;
    }
    ctx.req.params = match.params;

    let hi = 0;
    const next = async () => {
      if (hi < match.handlers.length) {
        await match.handlers[hi](ctx, () => { hi++; next(); });
      }
    };
    await next();
    return ctx;
  }
}

function bodyParser() {
  return async (ctx, next) => {
    if (ctx.req.method === 'POST' || ctx.req.method === 'PUT') {
      let raw = '';
      for await (const chunk of ctx.req.bodyStream || []) {
        raw += chunk;
      }
      try {
        ctx.req.body = JSON.parse(raw || '{}');
      } catch {
        ctx.req.body = {};
      }
    }
    await next();
  };
}

function authMiddleware(validTokens) {
  return async (ctx, next) => {
    const auth = ctx.req.headers?.['authorization'] || '';
    const token = auth.replace('Bearer ', '');
    if (!validTokens.includes(token)) {
      ctx.status = 401;
      ctx.body = { error: 'Unauthorized' };
      return;
    }
    ctx.req.user = { token };
    await next();
  };
}

function rateLimiter(maxReqs, windowMs) {
  const hits = new Map();
  setInterval(() => hits.clear(), windowMs);
  return async (ctx, next) => {
    const ip = ctx.req.ip || 'unknown';
    const count = (hits.get(ip) || 0) + 1;
    hits.set(ip, count);
    if (count > maxReqs) {
      ctx.status = 429;
      ctx.body = { error: 'Too Many Requests', retryAfterMs: windowMs };
      return;
    }
    await next();
  };
}

function validateJson(schema) {
  return async (ctx, next) => {
    if (!ctx.req.body) {
      await next();
      return;
    }
    const body = ctx.req.body;
    for (const [key, type] of Object.entries(schema)) {
      if (body[key] === undefined) {
        ctx.status = 400;
        ctx.body = { error: `Missing field: ${key}` };
        return;
      }
      if (typeof body[key] !== type) {
        ctx.status = 400;
        ctx.body = { error: `Field ${key} must be ${type}, got ${typeof body[key]}` };
        return;
      }
    }
    await next();
  };
}

async function demo() {
  const router = new Router();

  router.use(bodyParser());
  router.use(rateLimiter(10, 60000));
  router.use(authMiddleware(['valid-token-123']));

  router.get('/api/users', async (ctx) => {
    ctx.body = { users: [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }] };
  });

  router.get('/api/users/:id', async (ctx) => {
    ctx.body = { user: { id: parseInt(ctx.req.params.id), name: 'User' + ctx.req.params.id } };
  });

  router.post('/api/users',
    validateJson({ name: 'string', email: 'string' }),
    async (ctx) => {
      ctx.status = 201;
      ctx.body = { created: { id: 3, ...ctx.req.body } };
    }
  );

  const tests = [
    { method: 'GET', path: '/api/users', headers: { authorization: 'Bearer valid-token-123' } },
    { method: 'GET', path: '/api/users/42', headers: { authorization: 'Bearer valid-token-123' } },
    { method: 'POST', path: '/api/users', headers: { authorization: 'Bearer valid-token-123', 'content-type': 'application/json' }, bodyStream: [JSON.stringify({ name: 'Charlie', email: 'charlie@test.com' })] },
    { method: 'POST', path: '/api/users', headers: { authorization: 'Bearer valid-token-123' }, bodyStream: [JSON.stringify({ name: 'Diana' })] },
    { method: 'GET', path: '/api/users', headers: { authorization: 'Bearer bad-token' } },
    { method: 'GET', path: '/api/unknown', headers: { authorization: 'Bearer valid-token-123' } },
  ];

  for (const t of tests) {
    const ctx = await router.dispatch(t);
    console.log(`${t.method} ${t.path} -> ${ctx.status}`, JSON.stringify(ctx.body));
  }
}

if (require.main === module) {
  demo().catch(console.error);
}

module.exports = { Router, demo, authMiddleware, rateLimiter, validateJson, bodyParser };
