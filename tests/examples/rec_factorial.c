int find_factorial(int n){

   if(n == 0) {
      return(1);
    }

   return(n * find_factorial(n - 1));
}

int foo(int num, int fact)
{
   fact = find_factorial(num);

   return fact;
}

