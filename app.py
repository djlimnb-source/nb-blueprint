import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Blueprint Lite")

st.title("🎮 Unreal Blueprint Experience")
st.caption("화면이 안 나오면 새로고침을 해주세요. 마우스 우클릭으로 노드를 추가합니다.")

# 안정적인 동작을 위해 최신 버전 라이브러리 및 에러 방지 코드를 추가함
node_html = """
<html>
    <head>
        <style>
            body { margin: 0; background-color: #1a1a1a; overflow: hidden; }
            #rete { height: 100vh; width: 100vw; }
            /* 노드 스타일 살짝 보정 */
            .node { background: #333 !important; border: 1px solid #555 !important; }
        </style>
    </head>
    <body>
        <div id="rete"></div>

        <script src="https://cdn.jsdelivr.net/npm/vue@2.6.14/dist/vue.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/rete@1.4.5/build/rete.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/rete-vue-render-plugin@0.5.0/build/vue-render-plugin.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/rete-connection-plugin@0.9.0/build/connection-plugin.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/rete-context-menu-plugin@0.5.2/build/context-menu-plugin.min.js"></script>

        <script>
            const numSocket = new Rete.Socket('Number');

            class MyComponent extends Rete.Component {
                constructor() { super("BlueNode"); }
                builder(node) {
                    let inp = new Rete.Input('in', "Input", numSocket);
                    let out = new Rete.Output('out', "Output", numSocket);
                    return node.addInput(inp).addOutput(out);
                }
                worker(node, inputs, outputs) {}
            }

            async function init() {
                const container = document.querySelector('#rete');
                const editor = new Rete.NodeEditor('demo@0.1.0', container);
                
                editor.use(ConnectionPlugin.default);
                editor.use(VueRenderPlugin.default);
                editor.use(ContextMenuPlugin.default);

                const engine = new Rete.Engine('demo@0.1.0');
                const component = new MyComponent();
                editor.register(component);

                const n1 = await component.createNode();
                const n2 = await component.createNode();
                n1.position = [100, 100];
                n2.position = [400, 150];
                
                editor.addNode(n1);
                editor.addNode(n2);
                editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));
                
                editor.on('process nodecreated noderemoved connectioncreated connectionremoved', async () => {
                    await engine.abort();
                    await engine.process(editor.toJSON());
                });

                editor.view.resize();
                editor.trigger('process');
            }

            // 라이브러리 로드 대기 후 실행
            window.onload = init;
        </script>
    </body>
</html>
"""

# height를 700 정도로 넉넉히 주거나 스크롤을 방지합니다.
components.html(node_html, height=750, scrolling=False)