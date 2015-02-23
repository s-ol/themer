{# this goes in .themer/templates/i3/index.tpl #}
<html>
<body style="background: {{ background }}; color: {{ foreground }}; font: 12px monospace;">
<p>Default text will appear like this.</p>
 
<h3>Colors</h3>
<ul>
<li><p style="color: {{ white }}">White</p></li>
<li><p style="color: {{ alt_white }}">White (alt)</p></li>
<li><p style="color: {{ magenta }}">Magenta</p></li>
<li><p style="color: {{ alt_magenta }}">Magenta (alt)</p></li>
<li><p style="color: {{ blue }}">Blue</p></li>
<li><p style="color: {{ alt_blue }}">Blue (alt)</p></li>
<li><p style="color: {{ red }}">Red</p></li>
<li><p style="color: {{ alt_red }}">Red (alt)</p></li>
<li><p style="color: {{ green }}">Green</p></li>
<li><p style="color: {{ alt_green }}">Green (alt)</p></li>
<li><p style="color: {{ yellow }}">Yellow</p></li>
<li><p style="color: {{ alt_yellow }}">Yellow (alt)</p></li>
<li><p style="color: {{ cyan }}">Cyan</p></li>
<li><p style="color: {{ alt_cyan }}">Cyan (alt)</p></li>
<li><p style="color: {{ black }}">Black</p></li>
<li><p style="color: {{ alt_black }}">Black (alt)</p></li>
</ul>
 
<h3>Special</h3>
<ul>
<li><p style="color: {{ primary }}">Primary</p></li>
<li><p style="color: {{ secondary }}">Secondary</p></li>
<li><p style="color: {{ tertiary }}">Tertiary</p></li>
</ul>
 
<h3>Wallpaper</h3>
<ul>
<li><p style="color: {{ red }}">Left</p></li>
<li><p style="color: {{ green }}">Top</p></li>
<li><p style="color: {{ yellow }}">Right</p></li>
<li><p style="color: {{ magenta }}">Middle</p></li>
</ul>
 
</body>
</html>
