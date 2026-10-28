/* Adaptador de visualización gráfica offline de árboles.
 * vis-network se distribuye por separado bajo licencia MIT: vendor/LICENSE-vis-network-MIT.txt.
 * No altera los validadores del constructor ni interpreta HTML del proyecto.
 */
(function () {
  'use strict';
  const colors = {
    good:   { background: '#e4f4eb', border: '#168058', text: '#123a2a' },
    warn:   { background: '#fff2ce', border: '#996000', text: '#533500' },
    bad:    { background: '#ffe4e7', border: '#a22735', text: '#68141e' },
    unused: { background: '#edf0f2', border: '#77818b', text: '#3e4951' }
  };
  const symbols = { good: '✅', warn: '⚠', bad: '❌', unused: '◻' };
  let network = null;
  let edgeLimit = 8;
  let mode = 'graph';
  let current = null;
  const byId = (id) => document.getElementById(id);
  const clip = (text, length) => String(text || '').slice(0, length);

  function makeModel(analysis) {
    const nodes = [];
    const edges = [];
    const nodeKeys = new Set();
    const edgeTargets = new Map();
    let hidden = 0;

    function addNode(id, label, status) {
      if (nodeKeys.has(id)) return;
      nodeKeys.add(id);
      const color = colors[status] || colors.warn;
      nodes.push({
        id, label, shape: 'box', margin: 10, borderWidth: 2,
        widthConstraint: { maximum: 185 },
        color: { background: color.background, border: color.border },
        font: { face: 'Arial', size: 14, color: color.text }
      });
    }

    for (const n of state.nodes) {
      const status = !analysis.reachable.has(n.id) ? 'unused' : analysis.stateOf(n.id);
      const route = n.type === 'end' ? analysis.routes.get(n.routeId) : null;
      addNode('n:' + n.id,
        symbols[status] + (n.type === 'end' ? ' 🏁 ' : ' ❓ ') +
        clip(n.type === 'end' ? (route?.title || 'Sin ruta final') : (n.text || 'Sin pregunta'), 90),
        status);
    }

    for (const question of state.nodes.filter(n => n.type === 'question')) {
      question.options.forEach((option, index) => {
        if (index >= edgeLimit) { hidden++; return; }
        const status = analysis.edgeState(question, index);
        const color = colors[status] || colors.warn;
        let target = 'n:' + option.to;
        if (!option.to) {
          target = 'missing:' + question.id + ':' + index;
          addNode(target, '⚠ Falta conectar', status);
        } else if (!analysis.byId.has(option.to)) {
          target = 'unknown:' + option.to;
          addNode(target, '❌ Destino inexistente', status);
        }
        const edgeId = 'e:' + question.id + ':' + index;
        edges.push({
          id: edgeId, from: 'n:' + question.id, to: target,
          label: clip(option.label || 'Respuesta sin texto', 65),
          color: { color: color.border, hover: color.border, highlight: color.border },
          width: status === 'bad' ? 3 : 2,
          arrows: { to: { enabled: true, scaleFactor: 0.65 } },
          font: { color: color.text, background: '#f9fbfd', size: 12, align: 'middle', strokeWidth: 0 },
          smooth: { enabled: true, type: 'cubicBezier', forceDirection: 'vertical', roundness: 0.35 }
        });
        edgeTargets.set(edgeId, {
          kind: 'option', id: question.id, index,
          field: !option.label.trim() ? 'label' : 'to'
        });
      });
    }
    return { nodes, edges, edgeTargets, hidden };
  }

  function chooseMode(next) {
    if (next === 'graph' && (!window.vis || !window.vis.Network)) next = 'list';
    mode = next;
    byId('visPanel').hidden = mode !== 'graph';
    byId('flowCanvas').hidden = mode !== 'list';
    byId('visShowGraph').disabled = !window.vis || !window.vis.Network;
    byId('visShowGraph').setAttribute('aria-pressed', String(mode === 'graph'));
    byId('visShowList').setAttribute('aria-pressed', String(mode === 'list'));
    byId('visFit').hidden = mode !== 'graph';
    byId('visMore').hidden = mode !== 'graph';
    if (mode === 'graph' && network) network.redraw();
  }

  function redraw(analysis) {
    if (!window.vis || !window.vis.Network) {
      byId('visNotice').textContent = 'Grafo no disponible. La lista accesible sigue funcionando. El ZIP completo incluye vis-network.';
      chooseMode('list');
      return;
    }
    const model = makeModel(analysis);
    current = model;
    try {
      if (network) { network.destroy(); network = null; }
      network = new window.vis.Network(
        byId('visNetwork'), { nodes: model.nodes, edges: model.edges },
        {
          layout: { hierarchical: {
            enabled: true, direction: 'UD', sortMethod: 'directed', levelSeparation: 135,
            nodeSpacing: 190, treeSpacing: 200, edgeMinimization: true, blockShifting: true,
            parentCentralization: true
          }},
          physics: false,
          nodes: { shape: 'box' },
          interaction: { hover: true, dragNodes: false, navigationButtons: false, keyboard: false }
        }
      );
      network.on('click', params => {
        if (params.nodes && params.nodes.length) {
          const token = params.nodes[0];
          if (!token.startsWith('n:')) return;
          const node = analysis.byId.get(token.slice(2));
          if (!node) return;
          if (node.type === 'question') flowJump('question', node.id, 0, 'text');
          else {
            const route = analysis.routes.get(node.routeId);
            if (route) flowJump('route', route.id, 0, 'title');
          }
          return;
        }
        if (params.edges && params.edges.length) {
          const choice = current?.edgeTargets.get(params.edges[0]);
          if (choice) flowJump(choice.kind, choice.id, choice.index, choice.field);
        }
      });
      byId('visNotice').textContent = model.hidden
        ? model.hidden + ' respuestas ocultas en el grafo; utiliza «Mostrar respuestas». El validador revisa todas.'
        : 'Todas las respuestas representadas; selecciónalas para abrir su campo.';
      chooseMode(mode);
      if (mode === 'graph') network.fit({ animation: false });
    } catch (error) {
      if (network) { try { network.destroy(); } catch (_ignored) {} network = null; }
      byId('visNotice').textContent = 'No pudo dibujarse el grafo; usa la lista accesible.';
      chooseMode('list');
      console.warn('vis-network:', error.message);
    }
  }

  byId('visShowGraph').addEventListener('click', () => { mode = 'graph'; redraw(flowAnalyze()); });
  byId('visShowList').addEventListener('click', () => chooseMode('list'));
  byId('visFit').addEventListener('click', () => { if (network) network.fit({ animation: false }); });
  function zoom(factor) {
    if (network) network.moveTo({ scale: Math.max(0.05, Math.min(5, network.getScale() * factor)), animation: false });
  }
  function pan(x, y) {
    if (!network) return;
    const position = network.getViewPosition();
    const step = 80 / network.getScale();
    network.moveTo({ position: { x: position.x + x * step, y: position.y + y * step }, animation: false });
  }
  byId('visZoomIn').addEventListener('click', () => zoom(1.2));
  byId('visZoomOut').addEventListener('click', () => zoom(1 / 1.2));
  byId('visPanUp').addEventListener('click', () => pan(0, -1));
  byId('visPanDown').addEventListener('click', () => pan(0, 1));
  byId('visPanLeft').addEventListener('click', () => pan(-1, 0));
  byId('visPanRight').addEventListener('click', () => pan(1, 0));
  byId('visMore').addEventListener('click', () => { edgeLimit = Math.min(200, edgeLimit + 12); redraw(flowAnalyze()); });
  window.renderVisGraph = redraw;
  window.visGraphTestState = () => ({
    mode, hidden: current?.hidden ?? 0, nodes: current?.nodes.length ?? 0,
    edges: current?.edges.length ?? 0, library: Boolean(window.vis?.Network)
  });
})();
