---
layout: default
title: Aula Inteligente
permalink: /aula-inteligente/
description: "Noticias diarias, investigaciones y datos visuales sobre inteligencia artificial en la educación."
---
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="eyebrow">Aula Inteligente · IA educativa del Observatorio de IA</div>
      <h1>IA en la educación, con evidencia y criterio.</h1>
      <p class="hero-copy">Noticias diarias sobre inteligencia artificial en el sector educativo: aprendizaje, evaluación, docencia, investigación pedagógica y políticas educativas. Cada edición distingue hechos, estudios, declaraciones y debates, y convierte los datos importantes en gráficas fáciles de leer.</p>
      <div class="hero-actions">
        <a class="button" href="#ultimas">Ver últimas ediciones</a>
        <a class="button secondary" href="{{ '/ia-al-dia/' | relative_url }}">IA al Día · Noticias globales ↗</a>
        <a class="button secondary" href="{{ '/observatorio-ia/' | relative_url }}">Ver ambas líneas ↗</a>
      </div>
      <p class="adl-hero-message"><strong>Aprender primero.</strong> La IA debe apoyar el pensamiento, no sustituirlo.</p>
    </div>
    <aside class="hero-card">
      <span class="status-dot"></span>
      <strong>Actualización diaria · 8:15 a. m.</strong>
      <p>Noticias verificadas, fuentes directas, una visualización cuantitativa y una lectura práctica para docentes, estudiantes e instituciones.</p>
      <div class="mini-grid">
        <span>Aprendizaje</span><span>Evaluación</span><span>Docentes</span><span>Política</span><span>Privacidad</span><span>Equidad</span>
      </div>
    </aside>
  </div>
</section>

<section class="container section" id="ultimas">
  <div class="section-heading">
    <div>
      <div class="eyebrow">Archivo diario</div>
      <h2>Últimas ediciones</h2>
    </div>
    <p>Seguimiento breve y documentado de cómo la inteligencia artificial está cambiando la educación y de qué todavía no sabemos.</p>
  </div>

  {% assign aula_posts = site.posts | where_exp: "post", "post.categories contains 'aula-inteligente'" %}
  <div class="posts-grid">
  {% for post in aula_posts limit:30 %}
    <article class="post-card">
      <div class="post-date">{{ post.date | date: "%d/%m/%Y" }}</div>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.summary | default: post.excerpt | strip_html | truncate: 190 }}</p>
      {% if post.chart_image %}<p class="post-date">Incluye gráfica de datos</p>{% endif %}
      <a class="read-more" href="{{ post.url | relative_url }}">Leer edición →</a>
    </article>
  {% else %}
    <article class="post-card">
      <div class="post-date">Próximamente</div>
      <h3>La primera edición de Aula Inteligente se publicará automáticamente.</h3>
      <p>El flujo diario reunirá noticias de IA educativa, verificará las cifras y añadirá una gráfica con fuente y contexto.</p>
    </article>
  {% endfor %}
  </div>
</section>

<section class="principles">
  <div class="container section">
    <div class="eyebrow light">Principios editoriales</div>
    <h2>Datos antes que ruido.</h2>
    <div class="principles-grid">
      <div><strong>01</strong><h3>Fuentes directas</h3><p>Priorizamos investigaciones, organismos públicos, universidades y documentos originales.</p></div>
      <div><strong>02</strong><h3>Datos visibles</h3><p>Las cifras relevantes aparecen en gráficas legibles, con unidades, fuente y tamaño de muestra.</p></div>
      <div><strong>03</strong><h3>Uso pedagógico</h3><p>Explicamos qué significa cada desarrollo para enseñar, aprender y evaluar.</p></div>
      <div><strong>04</strong><h3>Incertidumbre clara</h3><p>Distinguimos hechos confirmados, resultados preliminares, proyecciones y controversias.</p></div>
    </div>
  </div>
</section>
