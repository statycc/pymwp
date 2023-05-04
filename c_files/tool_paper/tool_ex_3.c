/*
 * Tool paper section 2.1, example 3.
 */
void ex3(int X1, int X2, int X3)
{
   while(X2 < X1) { X2 = X1 + X1; }
   while(X3 < X2) { X3 = X2 + X2; }
   X3 = X3 * X3;
}