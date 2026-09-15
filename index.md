---
layout: default
title: Inicio
---
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="eyebrow">Observatorio educativo de Inteligencia Artificial</div>
      <h1>Entender la IA exige más que leer titulares.</h1>
      <p class="hero-copy">Cada día seleccionamos y explicamos las noticias de inteligencia artificial que ayudan a comprender qué está cambiando, qué preocupa a los expertos y qué vale la pena discutir en el aula.</p>
      <div class="hero-actions">
        <a class="button" href="#ultimas">Ver últimas ediciones</a>
        <a class="button secondary" href="{{ '/acerca/' | relative_url }}">Cómo funciona</a>
      </div>
    </div>
    <aside class="hero-card">
      <span class="status-dot"></span>
      <strong>Actualización diaria</strong>
      <p>Noticias recientes, fuentes enlazadas, riesgos, oportunidades y preguntas para estudiantes.</p>
      <div class="mini-grid">
        <span>Seguridad</span><span>Educación</span><span>Empleo</span><span>Regulación</span><span>Agentes</span><span>Sociedad</span>
      </div>
    </aside>
  </div>
</section>

<section class="container section" id="ultimas">
  <div class="section-heading">
    <div>
      <div class="eyebrow">Archivo</div>
      <h2>Últimas ediciones</h2>
    </div>
    <p>Los resúmenes distinguen hechos, estudios, declaraciones, proyecciones y controversias.</p>
  </div>

  <div class="posts-grid">
  {% for post in site.posts %}
    <article class="post-card">
      <div class="post-date">{{ post.date | date: "%d/%m/%Y" }}</div>
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p>{{ post.summary | default: post.excerpt | strip_html | truncate: 190 }}</p>
      <a class="read-more" href="{{ post.url | relative_url }}">Leer edición →</a>
    </article>
  {% else %}
    <article class="post-card">
      <div class="post-date">Próximamente</div>
      <h3>La primera edición se publicará desde GitHub Actions</h3>
      <p>Configura el secreto OPENAI_API_KEY y ejecuta manualmente el workflow para generar el primer resumen.</p>
    </article>
  {% endfor %}
  </div>
</section>

<section class="principles">
  <div class="container section">
    <div class="eyebrow light">Principios editoriales</div>
    <h2>Informar sin caer en el hype.</h2>
    <div class="principles-grid">
      <div><strong>01</strong><h3>Fuentes primero</h3><p>Las afirmaciones importantes deben estar respaldadas por fuentes identificables.</p></div>
      <div><strong>02</strong><h3>Contexto</h3><p>No basta con decir qué ocurrió: explicamos por qué importa y qué incertidumbres existen.</p></div>
      <div><strong>03</strong><h3>Uso educativo</h3><p>Cada edición propone preguntas que ayudan a convertir la noticia en aprendizaje.</p></div>
    </div>
  </div>
</section>
