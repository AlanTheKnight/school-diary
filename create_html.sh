cd school_diary/templates
name=""
read -p "Enter name of the file: " name
name="${name}.html"
cat <<EOT >> $name
{% extends 'base.html' %}
{% load static %}

{% block title %}
<title></title>
{% endblock %}

{% block content %}
<div class="container">

</div>
{% endblock %}
EOT
echo "done"