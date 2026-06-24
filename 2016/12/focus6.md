# 主題六：前端框架之爭

## 前端框架的 2016

2016 年是前端框架競爭白熱化的一年。React、Angular 2 和 Vue.js 三大框架各有特色，開發者需要根據專案需求做出選擇。

### 框架比較

```python
frameworks_2016 = {
    'React': {
        'company': 'Facebook',
        'version': '15.x',
        'strengths': ['元件化', 'Virtual DOM', '生態豐富'],
        'ideal_for': ['單頁應用', '大型專案', '需要高效能的場景'],
    },
    'Angular 2': {
        'company': 'Google',
        'version': '2.0',
        'strengths': ['完整方案', 'TypeScript', '企業支援'],
        'ideal_for': ['企業應用', '大型團隊', '需要嚴格架構的專案'],
    },
    'Vue.js': {
        'company': 'Community',
        'version': '2.0',
        'strengths': ['輕量', '易學', '漸進式'],
        'ideal_for': ['小型專案', '快速開發', '漸進式遷移'],
    },
}
```

## React

### React 核心概念

```jsx
// JSX 語法
import React from 'react';

class Counter extends React.Component {
    constructor(props) {
        super(props);
        this.state = { count: 0 };
    }

    increment = () => {
        this.setState({ count: this.state.count + 1 });
    }

    render() {
        return (
            <div>
                <h1>Count: {this.state.count}</h1>
                <button onClick={this.increment}>
                    Increment
                </button>
            </div>
        );
    }
}

export default Counter;
```

### Functional Component

```jsx
// Functional Component (React 14+)
const Greeting = ({ name }) => {
    return <h1>Hello, {name}!</h1>;
};

// Hooks (React 16.8+)
const Counter = () => {
    const [count, setCount] = React.useState(0);

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>
                Click
            </button>
        </div>
    );
};
```

### Virtual DOM

```python
virtual_dom_concept = """
Virtual DOM 的工作原理：

1. 狀態變化產生新的 Virtual DOM 樹
2. Diff 算法比較新舊 Virtual DOM
3. 只更新真正改變的實際 DOM
4. 減少昂貴的 DOM 操作
"""
```

## Angular 2

### Angular 核心概念

```typescript
// app.module.ts
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';
import { AppComponent } from './app.component';

@NgModule({
    imports: [BrowserModule, FormsModule],
    declarations: [AppComponent],
    bootstrap: [AppComponent]
})
export class AppModule { }
```

```typescript
// app.component.ts
import { Component } from '@angular/core';

@Component({
    selector: 'app-root',
    template: `
        <h1>{{ title }}</h1>
        <input [(ngModel)]="title" />
        <button (click)="onClick()">Click</button>
    `
})
export class AppComponent {
    title = 'Hello Angular';

    onClick() {
        console.log('Clicked!');
    }
}
```

### 服務和依賴注入

```typescript
// service
import { Injectable } from '@angular/core';

@Injectable()
export class DataService {
    private data: string[] = [];

    getData(): string[] {
        return this.data;
    }

    addData(item: string) {
        this.data.push(item);
    }
}

// component
@Component({
    selector: 'app-item',
    template: `<p>{{ item }}</p>`
})
export class ItemComponent {
    @Input() item: string;
}
```

## Vue.js

### Vue 核心概念

```html
<!-- Vue 實例 -->
<div id="app">
    <h1>{{ message }}</h1>
    <button @click="reverseMessage">Reverse</button>
</div>
```

```javascript
new Vue({
    el: '#app',
    data: {
        message: 'Hello Vue!'
    },
    methods: {
        reverseMessage() {
            this.message = this.message.split('').reverse().join('');
        }
    }
});
```

### Vue 元件

```javascript
// TodoItem.vue
<template>
    <li>{{ todo.text }}</li>
</template>

<script>
export default {
    props: ['todo']
}
</script>
```

### Vuex 狀態管理

```javascript
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        count: 0
    },
    mutations: {
        increment(state) {
            state.count++;
        }
    },
    actions: {
        incrementAsync({ commit }) {
            setTimeout(() => {
                commit('increment');
            }, 1000);
        }
    }
});
```

## 現代前端工具鏈

### 構建工具比較

```python
build_tools = {
    'Webpack': '功能強大，配置靈活，學習曲線陡',
    'Rollup': '適合函式庫，支持 tree-shaking',
    'Parcel': '零配置，自動處理',
    'Browserify': '簡單，社區成熟',
}
```

### NPM Scripts

```json
{
    "scripts": {
        "dev": "webpack --mode development",
        "build": "webpack --mode production",
        "test": "jest",
        "lint": "eslint src/**/*.js"
    }
}
```

## 選擇合適的框架

```python
def choose_framework(project):
    criteria = {
        'team_size': '大型團隊適合 Angular',
        'project_size': '小型專案適合 Vue',
        'performance': '需要高效能選 React',
        'learning_curve': '快速開發選 Vue',
        'ecosystem': '需要丰富資源選 React',
        'type_safety': '需要 TypeScript 選 Angular',
    }

    if project.get('enterprise'):
        return 'Angular 2'
    elif project.get('small'):
        return 'Vue.js'
    else:
        return 'React'
```

## 小結

2016 年的前端框架之爭沒有明確的贏家，每個框架都有其最適合的場景。React 繼續引領創新，Angular 2 為企業提供完整解決方案，Vue.js 以其簡潔贏得開發者青睞。選擇框架時，應根據團隊技能、專案需求和長期維護考慮，而非跟隨潮流。

---

**延伸閱讀**

- [React Documentation](https://www.google.com/search?q=React+official+documentation)
- [Angular Documentation](https://www.google.com/search?q=Angular+official+documentation)
- [Vue.js Documentation](https://www.google.com/search?q=Vue.js+official+documentation)