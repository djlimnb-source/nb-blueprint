import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="Blueprint Lite")

st.title("🎮 Unreal Blueprint Experience")
st.write("GitHub + Streamlit Cloud를 통한 노드 에디터 배포 테스트입니다.")

# Rete.js를 활용한 노드 에디터 소스
node_html = """
<div id="rete" style="height: 70vh; background: #1a1a1a; border-radius: 15px; border: 1px solid #333;"></div>
<script src="https://cdn.jsdelivr.net/npm/rete@1.4.5-rc.1/build/rete.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/rete-vue-render-plugin@0.5.1/build/vue-render-plugin.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/rete-connection-plugin@0.9.0/build/connection-plugin.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/rete-context-menu-plugin@0.5.2/build/context-menu-plugin.min.js"></script>

<script>
    const container = document.querySelector('#rete');
    const numSocket = new Rete.Socket('Value');

    class BlueComponent extends Rete.Component {
        constructor() { super("Logic Node"); }
        builder(node) {
            return node
                .addInput(new Rete.Input('in', "Input", numSocket))
                .addOutput(new Rete.Output('out', "Output", numSocket));
        }
        worker(node, inputs, outputs) {}
    }

    (async () => {
        const editor = new Rete.NodeEditor('demo@0.1.0', container);
        editor.use(ConnectionPlugin.default);
        editor.use(VueRenderPlugin.default);
        editor.use(ContextMenuPlugin.default);

        const engine = new Rete.Engine('demo@0.1.0');
        const comp = new BlueComponent();
        editor.register(comp);

        const n1 = await comp.createNode();
        const n2 = await comp.createNode();
        n1.position = [100, 100];
        n2.position = [400, 150];
        editor.addNode(n1);
        editor.addNode(n2);
        editor.connect(n1.outputs.get('out'), n2.inputs.get('in'));
        editor.view.resize();
    })();
</script>
"""

components.html(node_html, height=700)

st.markdown("""
---
**🕹️ 조작 가이드**
* **우클릭**: 새 노드 생성
* **드래그**: 노드 이동
* **선 연결**: 노드 끝 점을 드래그하여 연결
* **삭제**: 노드 선택 후 `Delete` 키
""")