// Funcio per a invertir una matriu MxM

#include <iostream>
#include <iomanip>
using namespace std;

/*{{{ funcio (double) inverteix */

double inverteix ( double arg1[5][5], double arg2[5][5], int N )

{

double factor, det = 1.0;

double A[5][10];

// Copiem i extenem la matriu original a A
for ( int i = 0; i < N ; i++ )
  { for ( int j = 0; j < N ; j++ )
      { A[j][i] = arg1[j][i];
        A[j][i+N] = 0.0;
      }

  A[i][i+N] = 1.0;
  }

// triangulem:
  for ( int i = 0; i < N ; i++ )
    for ( int j = i+1; j < N ; j++ )
      { factor = -A[j][i]/A[i][i];
        for ( int k = 0  ; k < 2*N ; k++ )
           A[j][k] = A[j][k] + factor*A[i][k] ;
      }

// determinant:
  for ( int i = 0; i < N ; i++ )
    { det *= A[i][i]; }

// diagonalitzem:
  for ( int i = N-1; i >= 0 ; i-- )
    for ( int j = i-1; j >= 0 ; j-- )
      { factor = -A[j][i]/A[i][i];
        for ( int k = 0  ; k < 2*N ; k++ )
           A[j][k] = A[j][k] + factor*A[i][k] ;
      }

// invertim:
  for ( int i = 0; i < N ; i++ )
    { factor = (double)1.0 / A[i][i];
        for ( int k = 0  ; k < 2*N ; k++ )
           A[i][k] *= factor ;
    }

// acabem la inversio:
  for ( int i = 0; i < N ; i++ )
    for ( int j = 0; j < N ; j++ )
      { arg2[i][j] = A[i][j+N] ;
      }

return det;

}
/*}}}*/

/*{{{ funcio (double) multiplica */

double multiplica ( double arg1[5][5], double arg2[5][5], double arg3[5][5], int N )

{

double residu = 0.0;

double aux ;

// fem la multiplicacio:
for ( int i = 0; i < N ; i++ )
  for ( int j = 0; j < N ; j++ )
  { arg3[j][i] = 0.0;
    for ( int k = 0; k < N ; k++ )
      { arg3[j][i] += arg1[j][k] * arg2[k][i] ;
      }
  }

// residu:
// diagonal:
  for ( int i = 0; i < N ; i++ )
    {
       aux = (arg3[i][i] - 1.0) * (arg3[i][i] - 1.0);
       if ( aux > residu )  residu = aux;
    }

// fora diagonal:
  for ( int i = 0; i < N ; i++ )
    for ( int j = 0; j < N ; j++ )
      {
         aux = arg3[i][j]  * arg3[i][j] ;
         if ( aux > residu ) 
           {  if ( i != j ) residu = aux;
           }
      }

return residu;

}

/*}}}*/


int main ()
{


int N=5;
double det;
double residu;

double A[5][5], B[5][5], C[5][5];

/*{{{ Inicialitzacio de la matriu A amb valors arbitraris */

// cout << "entra el num de files de la matriu, si's plau:" << '\n'
// cin >> N


// Inicialitzacio de la matriu A:

for ( int i = 0; i < N ; i++ )
  { for ( int j = 0; j < N ; j++ )
      { A[j][i] = 0.0;
      }

  A[i][i] = 1.0;
  }


A[0][0] = 1.0;
A[0][1] = 0.0;
A[1][0] = 2.0;
A[1][1] = 2.0;

/*}}}*/

cout.precision(4);

// calculem el determinant (det) i la inversa (B) de la matriu A:
det = inverteix ( A, B, N );
cout << "el determinant de A val " << det << '\n';

// comprovem el resultat, mesurant en el producte C = A.B (que hauria de ser la 
// matriu identitat) la maxima desviacio (residu).
residu = multiplica ( A, B, C, N );
cout << "el residu de A . B  val " << residu << '\n';

return 0;

}
