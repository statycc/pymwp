void t47(int n, int flag)
{
  flag = 1;

  while (flag>0) {
    if (n>0) {
      n = n - 1;
      flag=1;
    } else
      flag=0;
  }
}
