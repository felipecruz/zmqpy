test:
	py.test --verbos .

coverage:
	py.test --cov-report html --cov .

clean:
	rm -rf build/
	rm -rf __pycache__/
