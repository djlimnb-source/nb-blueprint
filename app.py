import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Blueprint Final")

st.title("🎮 블루프린트 표준 에디터 (에러 수정판)")

# 따옴표 문제를 방지하기 위해 HTML을 리스트로 나누어 결합합니다.
html_parts = [
    "<!DOCTYPE html><html><head><style>",
    "body { margin: 0; background-color: #1a1a1a; overflow: hidden; font-family: sans-serif; }",
    "#rete { height: 100vh; width: 100vw; }",
    ".connection .main-path { stroke: #666; stroke-width: 4px !important; transition: all 0.2s; cursor: pointer; }",
    ".connection.selected .main-path { stroke: #ff9d00 !important; filter: drop-shadow(0 0 8px #ff9d00); stroke-width: 6px !important; }",
    ".node { background: #252525 !important; border: 1px solid #444 !important; border-radius: 8px !important; }",
    ".node.selected { border: 2px solid #ff9d00 !important; }",
    ".node .title { background: #333 !important; color: #eee !important; padding: 10px !important; font-size: 14px; border-radius: 6px 6px 0 0; }",
    ".socket { width: 16px !important; height: 16px !important; margin: 6px !important; }",
    "</style></head><body><div id='rete'></div>",
    "<script src='https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.min.js'></script>",
    "<script src='https://cdn.jsdelivr.net/npm/rete@1.4.5/build/rete.min.js'></script>",
    "<script src='https://cdn.jsdelivr.net/npm/rete-vue-render-plugin@0.5.0/build/vue-render-plugin.min.js'></script>",
    "<script src='https://cdn.jsdelivr.net/npm/rete-connection-plugin@0.9.0/build/connection-plugin.min.js'></script>",
    "<script src='https://cdn.jsdelivr.net/npm/rete-context-menu-plugin@0.5.2/build/context-menu-plugin.min.js'></script>",
    "<script>",
    "const numSocket = new Rete.Socket('Data');",
    "class BlueNode extends Rete.Component { constructor() { super('Node'); } builder(node) { return node.addInput(new Rete.Input('in', 'Input', numSocket)).addOutput(new Rete.Output('out', 'Output', numSocket)); } }",
    "async function init() {",
    "  const container = document.querySelector('#rete');",
    "  const editor = new Rete.NodeEditor('demo@0.1.0', container);",
    "  editor.use(ConnectionPlugin.default, { curvature: 0.4, interactive: true });",
    "  editor.use(VueRenderPlugin.default); editor.use(ContextMenuPlugin.default);",
    "  const component = new BlueNode(); editor.register(component);",
    "  const n1 = await component.createNode({ x: 100, y: 150 });",
    "  const n2 = await component.createNode({ x: 450, y: 300 });",
    "  const n3 = await component.createNode({ x: 800, y: 150 });",
    "  editor.addNode(n1); editor.addNode(n2); editor.addNode(n3);",
    "  editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));",
    "  editor.connect(n2.outputs.get('out'), n3.inputs.get('in'));",
    "  let currentSelectedConn = null;",
    "  editor.on('connectionpick', (c) => {",
    "    if (currentSelectedConn) { const v = editor.view.connections.get(currentSelectedConn); if(v) v.el.classList.remove('selected'); }",
    "    currentSelectedConn = c; const v = editor.view.connections.get(c); if(v) v.el.classList.add('selected');",
    "    return true;",
    "  });",
    "  editor.on('click', () => { if (currentSelectedConn) { const v = editor.view.connections.get(currentSelectedConn); if(v) v.el.classList.remove('selected'); currentSelectedConn = null; } });",
    "  window.addEventListener('keydown', e => { if (e.key === 'Delete' || e.key === 'Backspace') { editor.selected.each(node => editor.removeNode(node)); if (currentSelectedConn) { editor.removeConnection(currentSelectedConn); currentSelectedConn = null; } } });",
    "  editor.view.resize();",
    "}",
    "window.onload = init;",
    "</script></body></html>"
]

# 모든 조각을 하나의 문자열로 합칩니다.
node_editor_code = "".join(html_parts)

# 최종 렌더링
components.html(node_editor_code, height=750, scrolling=False)