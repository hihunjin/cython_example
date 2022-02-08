# Cythonize example

1. Run test

```python
python main.py
```

2. cythonize

```python
python setup.py build_ext --**inplace**
```

3. Run test again with ``.so``
   
```python
python main.py
```