import sys

def check_sys_requirements() -> None:

  s = sys.version.split(' ')[0]

  get_version = lambda version: [int(x) for x in version.split('.')]

  required_py = '3.10.6' # 3.10.7 is required so < 3.10.6 error

  ra, rb, rc = get_version(required_py)

  va, vb, vc = get_version(s)

  for r, v in zip([ra, rb, rc], [va, vb, vc]):

    if v > r:

      break

  else:

    raise Exception(
        f'Python Version > {required_py} required, not version {s}'
    )

  return

if __name__ == '__main__':

    check_sys_requirements()