---
layout: default
title: Inicio
---
<section class="hero">
  <div class="container hero-grid">
    <div>
      <div class="eyebrow">Observatorio educativo de Inteligencia Artificial</div>
      <h1>Entender la IA exige más que leer titulares.</h1>
      <p class="hero-copy">Cada semana seleccionamos y explicamos las noticias de inteligencia artificial más importantes y críticas para comprender qué está cambiando, qué preocupa a los expertos y qué vale la pena discutir en el aula.</p>
      <div class="hero-actions">
        <a class="button" href="#ultimas">Ver últimos consolidados</a>
        <a class="button secondary" href="#infografias">Ver infografías</a>
        <a class="button secondary" href="{{ '/acerca/' | relative_url }}">Cómo funciona</a>
      </div>
    </div>
    <aside class="hero-card">
      <span class="status-dot"></span>
      <strong>Actualización semanal · domingos 8:00 a. m.</strong>
      <p>Noticias clave de la semana, fuentes enlazadas, nivel de criticidad, riesgos, oportunidades, preguntas para estudiantes y una infografía visual de síntesis.</p>
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
    <p>Los consolidados distinguen hechos, estudios, declaraciones, proyecciones y controversias, y priorizan los asuntos con mayor impacto de la semana.</p>
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
      <h3>El primer consolidado semanal se publicará desde GitHub Actions</h3>
      <p>El flujo automático genera cada domingo un nuevo resumen de las noticias más importantes de inteligencia artificial.</p>
    </article>
  {% endfor %}
  </div>
</section>

<section class="infographics-section" id="infografias">
  <div class="container section">
    <div class="section-heading">
      <div>
        <div class="eyebrow">Resumen visual</div>
        <h2>Infografías semanales</h2>
      </div>
      <p>Cada consolidado semanal se convierte también en una pieza visual pensada para lectura rápida, clase y difusión en redes o mensajería.</p>
    </div>

    {% if site.data.infografias and site.data.infografias.size > 0 %}
      {% assign infografias = site.data.infografias | reverse %}
      <div class="infographics-grid">
      {% for item in infografias limit:6 %}
        <article class="infographic-card">
          <a class="infographic-image" href="{{ item.image | relative_url }}" target="_blank" rel="noopener">
            <img src="{{ item.image | relative_url }}" alt="{{ item.alt | escape }}" loading="lazy">
          </a>
          <div class="infographic-copy">
            <div class="post-date">{{ item.date | date: "%d/%m/%Y" }}</div>
            <h3>{{ item.title }}</h3>
            <p>Resumen visual de las noticias, riesgos y oportunidades clave del periodo.</p>
            <div class="infographic-actions">
              <a class="read-more" href="{{ item.image | relative_url }}" target="_blank" rel="noopener">Abrir infografía ↗</a>
              <a class="read-more muted-link" href="{{ item.post_url | relative_url }}">Leer noticias →</a>
            </div>
          </div>
        </article>
      {% endfor %}
      </div>
    {% else %}
      <div class="empty-infographic">
        <strong>La primera infografía semanal se generará automáticamente.</strong>
        <p>Cuando exista un consolidado semanal, el flujo creará su resumen visual y lo mostrará aquí.</p>
      </div>
    {% endif %}
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
