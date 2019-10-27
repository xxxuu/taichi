import taichi as ti

@ti.program_test
def test_loop_grad():
  ti.set_gdb_trigger()
  ti.cfg.print_ir = True
  x = ti.var(ti.f32)

  n = 16
  m = 8

  @ti.layout
  def place():
    ti.root.dense(ti.ij, (n, m)).place(x)
    ti.root.lazy_grad()

  @ti.kernel
  def func():
    for k in range(n):
      for i in range(m - 1):
        x[k, i + 1] = x[k, i] * 2


  for k in range(n):
    x[k, 0] = k
  func()

  for k in range(n):
    x.grad[k, m - 1] = 1
  func.grad()

  for k in range(n):
    for i in range(m):
      assert x[k, i] == 2 ** i * k
      assert x.grad[k, i] == 2 ** (m - 1 - i)


@ti.program_test
def test_loop_grad_complex():
  return # This case is not supported yet
  x = ti.var(ti.f32)

  n = 16
  m = 8
  @ti.layout
  def place():
    ti.root.dense(ti.ij, (n, m)).place(x)
    ti.root.lazy_grad()

  @ti.kernel
  def func():
    for k in range(n):
      t = k * k
      tt = t * 2
      for i in range(m - 1):
        x[k, i + 1] = x[k, i] * 2 + tt


  for k in range(n):
    x[k, 0] = k
  func()

  for k in range(n):
    x.grad[k, m - 1] = 1
  func.grad()

  for k in range(n):
    for i in range(m):
      assert x[k, i] == i ** 2 + 2 * k ** 2
      assert x.grad[k, i] == 2 ** (m - 1 - i)

