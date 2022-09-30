---
layout: post
title:  "Ansible naming conventions"
date:   2022-09-20 15:14:43 +0200
tags: ansible coding-conventions
description: A quick look at what can be found in Ansible related documentation regarding naming conventions (roles, tasks, ...)
---

Having understood the default [Ansible directory layout](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html#directory-layout){:target="_blank"} and discovered ansible-galaxy can create part of this layout automatically (e.g for a role: `ansible-galaxy init test-role`), remains the question of naming conventions in Ansible.  
<br/>
Here's what could be found in Ansible related documentation:  

* Roles name
    * From Ansible Galaxy documentation ([source](https://galaxy.ansible.com/docs/contributing/creating_role.html#role-names){:target="_blank"}): `Role names are limited to lowercase word characters (i.e., a-z, 0-9) and ‘_’. No special characters are allowed, including ‘.’, ‘-‘, and space`.
    * From Ansible devel documentation ([source](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections_structure.html#roles-directory){:target="_blank"}) as spotted by Ansible Lint documentation ([source](https://ansible-lint.readthedocs.io/rules/role-name/){:target="_blank"}): `Role names are now limited to contain only lowercase alphanumeric characters, plus _ and start with an alpha character`.  
<br/>

* Variables name: 
    * From Ansible documentation ([source](https://docs.ansible.com/ansible/latest/user_guide/playbooks_variables.html#creating-valid-variable-names){:target="_blank"}): `A variable name can only include letters, numbers, and underscores. Python keywords or playbook keywords are not valid variable names. A variable name cannot begin with a number. Variable names can begin with an underscore. In many programming languages, variables that begin with an underscore are private. This is not true in Ansible`.
    * From Ansible lint documentation ([source](https://ansible-lint.readthedocs.io/rules/var-naming/){:target="_blank"}): `All variables should be named using only lowercase and underscores`.
    * Regarding variable names many third party sources recommend to prepend variable used in a role with the role name (e.g `apache_max_keepalive`).  
<br/>

* Yaml files name: 
    * For tasks, playbook and other yaml files, I was not able to find a proper naming convention.
    * From Ansible lint documentation ([source](https://ansible-lint.readthedocs.io/rules/playbook-extension/){:target="_blank"}) `Playbooks should have the ".yml" or ".yaml" extension`.
    * From this Ansible documentation example ([source](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html#ansible-lint){:target="_blank"}), it seems playbook file names may include a `-` 🤔  
<br/>

* `name:` keys in tasks and playbooks yaml files:
    * From Ansible Lint ([source](https://ansible-lint.readthedocs.io/rules/name/){:target="_blank"}): `All names should start with an uppercase letter for languages that support it`. Here `language` obviously means natural human languages (english, german, french, ...).
<br/>

Sticking to [snake-case](https://en.wikipedia.org/wiki/Snake_case){:target="_blank"} should be the best solution when working with Ansible. No surprises for a Python project.
