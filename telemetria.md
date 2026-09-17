---
layout: default
title: Telemetría
permalink: /telemetria/
---

<section class="page container narrow">
  <div class="eyebrow">Transparencia operativa</div>
  <h1>Telemetría del agente</h1>
  <p class="lead">Este panel registra el consumo reportado por la API durante la generación automática de <strong>IA al Día</strong>: tokens de entrada y salida, búsquedas web y costo estimado de cada edición.</p>

  {% assign registros = site.data.consumo_api %}
  {% assign ultimo = registros | last %}

  {% if ultimo %}
  <div class="info-grid" style="margin: 1.5rem 0 2rem 0;">
    <div class="info-card">
      <h3>Última ejecución</h3>
      <p><strong>{{ ultimo.date }}</strong><br>Estado: {% if ultimo.status == 'success' %}✅ Correcta{% else %}⚠️ {{ ultimo.status }}{% endif %}</p>
    </div>
    <div class="info-card">
      <h3>Tokens</h3>
      <p>Entrada: <strong>{{ ultimo.input_tokens | default: 0 }}</strong><br>Salida: <strong>{{ ultimo.output_tokens | default: 0 }}</strong></p>
    </div>
    <div class="info-card">
      <h3>Búsquedas web</h3>
      <p><strong>{{ ultimo.web_search_calls | default: 0 }}</strong> llamadas</p>
    </div>
    <div class="info-card">
      <h3>Costo estimado</h3>
      <p>Edición: <strong>US$ {{ ultimo.estimated_cost_usd | default: 0 }}</strong><br>Mes: <strong>US$ {{ ultimo.month_estimated_cost_usd | default: 0 }}</strong></p>
    </div>
  </div>
  {% endif %}

  <h2>Histórico</h2>
  <div style="overflow-x:auto;">
    <table style="width:100%; border-collapse:collapse;">
      <thead>
        <tr>
          <th style="text-align:left; padding:.65rem; border-bottom:2px solid #dbe5ee;">Fecha</th>
          <th style="text-align:left; padding:.65rem; border-bottom:2px solid #dbe5ee;">Estado</th>
          <th style="text-align:right; padding:.65rem; border-bottom:2px solid #dbe5ee;">Entrada</th>
          <th style="text-align:right; padding:.65rem; border-bottom:2px solid #dbe5ee;">Salida</th>
          <th style="text-align:right; padding:.65rem; border-bottom:2px solid #dbe5ee;">Web</th>
          <th style="text-align:right; padding:.65rem; border-bottom:2px solid #dbe5ee;">Costo estimado</th>
        </tr>
      </thead>
      <tbody>
        {% assign invertidos = registros | reverse %}
        {% for item in invertidos limit:30 %}
        <tr>
          <td style="padding:.65rem; border-bottom:1px solid #e7edf3;">{{ item.date }}</td>
          <td style="padding:.65rem; border-bottom:1px solid #e7edf3;">{% if item.status == 'success' %}✅ success{% else %}⚠️ {{ item.status }}{% endif %}</td>
          <td style="text-align:right; padding:.65rem; border-bottom:1px solid #e7edf3;">{{ item.input_tokens | default: 0 }}</td>
          <td style="text-align:right; padding:.65rem; border-bottom:1px solid #e7edf3;">{{ item.output_tokens | default: 0 }}</td>
          <td style="text-align:right; padding:.65rem; border-bottom:1px solid #e7edf3;">{{ item.web_search_calls | default: 0 }}</td>
          <td style="text-align:right; padding:.65rem; border-bottom:1px solid #e7edf3;">US$ {{ item.estimated_cost_usd | default: 0 }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  <h2>Cómo se calcula</h2>
  <p>La telemetría usa los contadores de <code>usage</code> devueltos por la Responses API. Se separan tokens de entrada normales, tokens en caché, escrituras de caché, tokens de salida y llamadas de búsqueda web. El costo mostrado es una <strong>estimación técnica</strong> calculada con las tarifas configuradas en el agente; la facturación oficial de OpenAI es la referencia definitiva.</p>

  <p>Para GPT-5.6 Luna, el agente tiene configuradas las tarifas Standard vigentes al 17 de septiembre de 2026 y el costo de búsqueda web correspondiente. Si el modelo cambia y no existe una tarifa configurada, los tokens seguirán registrándose pero el costo aparecerá sin estimar.</p>

  <p><a href="https://developers.openai.com/api/docs/pricing" target="_blank" rel="noopener">Consultar tarifas oficiales de OpenAI API ↗</a></p>

  <div class="info-card" style="margin-top:1.5rem;">
    <h3>Importante</h3>
    <p>La telemetría comienza el 17 de septiembre de 2026. Las ediciones anteriores no guardaron métricas de uso, por lo que no se reconstruyen cifras que la API no haya reportado.</p>
  </div>
</section>
