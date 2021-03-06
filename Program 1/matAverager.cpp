//Most of this code by Professor Mark McKenny
//Averaging algorithm by Dane Johnson
#include <sys/time.h>
#include <fstream>
#include <iostream>
#include <omp.h>
#include <cstdlib>
#include <sstream>
#include <string>

using namespace std;

typedef unsigned int ** val;
typedef double ** sol;

struct ordered_pair
{
	int x;
	int y;
	ordered_pair(){
		x = 1;
		y = 1;
	}
	ordered_pair(int init_x, int init_y)
	{
		x = init_x;
		y = init_y;
	}
};

double findmaxavg(val, const int&, const int&, ordered_pair&);
void populateSolCenter(val, const int&, const int&, sol);
void populateSolTopEdge(val, const int&, const int&, sol);
void populateSolBottomEdge(val, const int&, const int&, sol);
void populateSolLeftEdge(val, const int&, const int&, sol);
void populateSolRightEdge(val, const int&, const int&, sol);
//double findlocalavg(val, const int&, const int&, const int&, const int&);

// a class to get more accurate time

class stopwatch{
	
private:
	double elapsedTime;
	double startedTime;
	bool timing;
	//returns current time in seconds
	double current_time( ) 
	{
		timeval tv;
		gettimeofday(&tv, NULL);
		double rtn_value = (double) tv.tv_usec;
		rtn_value /= 1e6;
		rtn_value += (double) tv.tv_sec;
		return rtn_value;
	}
	
public:
	stopwatch( ): elapsedTime( 0 ), startedTime( 0 ), timing( false )
	{
		
	}
	
	void start( )
	{
		if( !timing )
		{
			timing = true;
			startedTime = current_time( );
		}
	}
	
	void stop( )
	{
		if( timing )
		{
			elapsedTime +=  current_time( )-startedTime;
			timing = false;
		}
	}
	
	void resume( )
	{
		start( );
	}
	
	void reset( )
	{
		elapsedTime = 0;
		startedTime = 0;
		timing = false;
	}
	
	double getTime( )
	{
		return elapsedTime;
	}
};



// function takes an array pointer, and the number of rows and cols in the array, and 
// allocates and intializes the two dimensional array to a bunch of random numbers

void makeRandArray( unsigned int **& data, unsigned int rows, unsigned int cols, unsigned int seed )
{
	// allocate the array
	data = new unsigned int*[ rows ];
	for( unsigned int i = 0; i < rows; i++ )
	{
		data[i] = new unsigned int[ cols ];
	}
	
	// seed the number generator
	// you should change the seed to get different values
	srand( seed );
	
	// populate the array
	
	for( unsigned int i = 0; i < rows; i++ )
		for( unsigned int j = 0; j < cols; j++ )
		{
			data[i][j] = rand() % 10000 + 1; // number between 1 and 10000
		}
	
}

void getDataFromFile( unsigned int **& data, char fileName[], unsigned int &rows, unsigned int &cols )
{
	ifstream in;
	in.open( fileName );
	if( !in )
	{
		cerr << "error opening file: " << fileName << endl;
		exit( -1 );
	}
	
	in >> rows >> cols;
	data = new unsigned int*[ rows ];
	for( unsigned int i = 0; i < rows; i++ )
	{
		data[i] = new unsigned int[ cols ];
	}
	
	// now read in the data
	
	for( unsigned int i = 0; i < rows; i++ )
		for( unsigned int j = 0; j < cols; j++ )
		{
			in >> data[i][j];
		}
	
}


int main( int argc, char* argv[] ) 
{
	if( argc < 3 )
	{
		cerr<<" usage: exe [input data file] [num of threads to use] " << endl;
		
		cerr<<"or usage: exe rand [num of threads to use] [num rows] [num cols] [seed value]" << endl;
	}
	
	// read in the file
	unsigned int rows, cols, seed;
	unsigned int numThreads;
	unsigned int ** data;
	// convert numThreads to int
	{
		stringstream ss1;
		ss1 << argv[2];
		ss1 >> numThreads;
	}
	
	string fName( argv[1] );
	if( fName == "rand" )
	{
		{
			stringstream ss1;
			ss1 << argv[3];
			ss1 >> rows;
		}
		{
			stringstream ss1;
			ss1 << argv[4];
			ss1 >> cols;
		}
		{
			stringstream ss1;
			ss1 << argv[5];
			ss1 >> seed;
		}
		makeRandArray( data, rows, cols, seed );
	}
	else
	{
		getDataFromFile( data,  argv[1], rows, cols );
	}
	
		//cerr << "data: " << endl;
	 for( unsigned int i = 0; i < rows; i++ )
	 {
	 for( unsigned int j = 0; j < cols; j++ )
	 {
	 //cerr << "i,j,data " << i << ", " << j << ", ";
	 //cerr << data[i][j] << " ";
	 }
	 //cerr << endl;
	 }
	 //cerr<< endl;
	
	// tell omp how many threads to use
	omp_set_num_threads( numThreads );
	
	stopwatch S1;
	S1.start();
	
	double avg;
	ordered_pair pair;
	
	avg = findmaxavg(data, rows, cols, pair);
	
	S1.stop();
	
	// print out the max value here
	
	cout << "largest average: " << avg << endl;
	cout << "found at cell: (" << pair.x << ", " << pair.y << ")" << endl ;
	// //while(!pairs.empty())
	// //{
		// ordered_pair curr = pairs.front();
		// cout << "(" << curr.x << ", " << curr.y <<")  ";
		// pairs.pop_front();
	// }
	//cout << endl;
	cerr << "elapsed time: " << S1.getTime( ) << endl;
}

//finds max average iteratively
double findmaxavg(val data, const int& rows, const int& cols, ordered_pair& pair)
{
	//double max = findlocalavg(data, 0, 0, rows, cols); //set first value to max
	// pairs.push_front(ordered_pair(0, 0));
	
	// #pragma omp parallel for
	// for(int i = 0; i < rows; i++)
	// {
		// for(int j = 0; j < cols; j++)
		// {
			// double test = findlocalavg(data, i, j, rows, cols); //get the local average
			// if(test > max)
			// {
				// #pragma omp critical
				// {
					// if(test > max)
					// {
						// max = test; // if it's better, replace it
						// pairs.clear();
						// pairs.push_front(ordered_pair(i, j));
					// }
				// }
			// } 
		// }
	// }
	// #pragma omp barrier
	
	sol solution = new double* [rows];
	#pragma omp parallel for
	for (int i = 0; i < rows; i++)
	{
		solution[i] = new double[cols];
	}
	
	populateSolCenter(data, rows, cols, solution);
	populateSolRightEdge(data, rows, cols, solution);
	populateSolLeftEdge(data, rows, cols, solution);
	populateSolTopEdge(data, rows, cols, solution);
	populateSolBottomEdge(data, rows, cols, solution);
	
	solution[0][0] = double(data[0][0] + data[0][1] + data[1][0] + data[1][1]) / 4;
	solution[rows - 1][0] = double(data[rows - 1][0] + data[rows - 1][1] + data[rows - 2][0] + data[rows - 2][1]) / 4;
	solution[0][cols - 1] = double(data[0][cols - 1] + data[1][cols - 1] + data[0][cols - 2] + data[1][cols - 2]) / 4;
	solution[rows - 1][cols - 1] = double(data[rows - 1][cols - 1] + data[rows - 1][cols - 2] + data[rows - 2][cols - 1] + data[rows - 2][cols - 2]) / 4;
	
	double maximum = 0.0;
	#pragma omp parallel for
	for(int i = 0; i < rows; i++)
	{
		for(int j = 0; j < cols; j++)
		{
			if(solution[i][j] > maximum)
			{
				#pragma omp critical
				{
					if(solution[i][j] > maximum)
					{
						maximum = solution[i][j];
						pair.x = i;
						pair.y = j;
					}
				}
			}
		}
	}
	
	return maximum;
}

void populateSolCenter(val data, const int& rows, const int& cols, sol solution)
{
	#pragma omp parallel for
	for(int i = 1; i < rows - 1; i++)
	{
		for(int j = 1; j < cols - 1; j++)
		{
			solution[i][j] = double(
				data[i - 1][j - 1] + data[i][j - 1] + data[i + 1][j - 1] +
				data[i - 1][j]     + data[i][j]     + data[i + 1][j] +
				data[i - 1][j + 1] + data[i][j + 1] + data[i + 1][j + 1]
				) / 9;
		}
	}
}

void populateSolTopEdge(val data, const int& rows, const int& cols, sol solution)
{
	#pragma omp parallel for
	for(int i = 1; i < cols - 1; i++)
	{
		solution[0][i] = double(
				data[0][i - 1] + data[0][i] + data[0][i + 1] +
				data[1][i - 1] + data[1][i] + data[1][i + 1]
			) / 6;
			
	}
}

void populateSolLeftEdge(val data, const int& rows, const int& cols, sol solution)
{
	#pragma omp parallel for
	for(int i = 1; i < rows - 1; i++)
	{
		solution[i][0] = double(
				data[i - 1][0] + data[i][0] + data[i + 1][0] +
				data[i - 1][1] + data[1][1] + data[i + 1][1]
			) / 6;
	}
}

void populateSolBottomEdge(val data, const int& rows, const int& cols, sol solution)
{
	#pragma omp parallel for
	for(int i = 1; i < cols - 1; i++)
	{
		solution[rows - 1][i] = double(
				data[rows - 1][i - 1] + data[rows - 1][i] + data[rows - 1][i + 1] +
				data[rows - 2][i - 1] + data[rows - 2][i] + data[rows - 2][i + 1]
			) / 6;
			
	}
}

void populateSolRightEdge(val data, const int& rows, const int& cols, sol solution)
{
	#pragma omp parallel for
	for(int i = 1; i < rows - 1; i++)
	{
		solution[i][cols - 1] = double(
				data[i - 1][cols - 1] + data[i][cols - 1] + data[i + 1][cols - 1] +
				data[i - 1][cols - 2] + data[1][cols - 2] + data[i + 1][cols - 2]
			) / 6;
	}
}
// double findlocalavg(val data, const int& i, const int& j, const int& rows, const int& cols)
// {
	// int nvals = 1, total = data[i][j]; //We have at least one value
	// bool isTop = (j == 0), isBottom = (j + 1 == cols), isLeftEdge = (i == 0), isRightEdge = (i + 1 == rows);
	// if(!isLeftEdge) //We're clear to the left
	// {
		// nvals++;
		// total += data[i - 1][j];
		// if(!isTop)//Top left clear
		// {
			// nvals++;
			// total += data[i - 1][j - 1];
		// }
		// if(!isBottom)//Bottom left clear
		// {
			// nvals++;
			// total += data[i - 1][j + 1];
		// }
	// }
	// if(!isRightEdge) //We're clear to the right
	// {
		// nvals++;
		// total += data[i + 1][j];
		// if(!isTop)//Top right clear
		// {
			// nvals++;
			// total += data[i + 1][j - 1];
		// }
		// if(!isBottom)//Bottom right clear
		// {
			// nvals++;
			// total += data[i + 1][j + 1];
		// }
	// }
	// if(!isTop) //Top clear
	// {
		// nvals++;
		// total += data[i][j - 1];
	// }
	// if(!isBottom)
	// {
		// nvals++;
		// total += data[i][j + 1];
	// }
	
	// return double(total) / nvals;
// }


