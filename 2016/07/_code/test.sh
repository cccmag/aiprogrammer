set -x
python3 -m http.server 8000 &
sleep 2
open http://localhost:8000/_code/webgl-demo.html
echo "Demo running at http://localhost:8000/_code/webgl-demo.html"