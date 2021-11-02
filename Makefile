play:
	ANSIBLE_PYTHON_INTERPRETER=$$(pwd)/venv/bin/python ansible-playbook -c local -i inventory playbook.yml
