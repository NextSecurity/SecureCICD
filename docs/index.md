---
layout: default
title: SecureCICD Blog
---

# 🧠 SecureCICD Blog

Welcome to the SecureCICD blog — by **NextSecurity**.

We publish short, focused posts on securing modern CI/CD pipelines:
- Preventing self-approval abuse
- Detecting approval reassignment
- Enforcing runtime SoD (separation of duties)

Explore all posts below 👇

<ul>
{% for post in site.posts %}
  <li>
    <a href="{{ post.url }}">{{ post.title }}</a> — {{ post.date | date: "%Y-%m-%d" }}
  </li>
{% endfor %}
</ul>
