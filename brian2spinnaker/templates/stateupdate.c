/*
 * TODO:
 * - Define REAL as scalar/double/float/whatever
 * - Define REAL_CONST( x ) x##f // depends on data type
 * - h is the timestep
 * - exc_input is coming from ring buffer: need to work through code to find out where
 */

#include "stateupdate.h"

bool neuron_state_update( REAL exc_input, REAL inh_input, REAL external_bias, neuron_pointer_t neuron )
{

	//input_this_timestep is statically defined somewhere and is used in several places

	//input_this_timestep = exc_input - inh_input + external_bias + neuron->I_offset; 	// all need to be in nA


	//////////////// TODO: Insert state update here
	{{ vector_code | autoindent }}

	REAL 	lastV1 = neuron->V, lastU1 = neuron->U, a = neuron->A, b = neuron->B;  // to match Mathematica names

	REAL	pre_alph = REAL_CONST(140.0) + input_this_timestep - lastU1,
			alpha = pre_alph + ( REAL_CONST(5.0) + REAL_CONST(0.0400) * lastV1 ) * lastV1,
			eta = lastV1 + REAL_HALF( h * alpha ),
			beta = REAL_HALF( h * ( b * lastV1 - lastU1 ) * a ); // could be represented as a long fract?

//	neuron->V = lastV1 +
	neuron->V +=
					h * ( pre_alph - beta + ( REAL_CONST(5.0) + REAL_CONST(0.0400) * eta ) * eta );

//	neuron->U = lastU1 +
	neuron->U +=
					a * h * ( -lastU1 - beta + b * eta );


   ///////////// TODO: This is the threshold
   //bool spike = REAL_COMPARE( noisy_membrane, >=, V_threshold ); // more efficient
   bool spike = noisy_membrane >= V_threshold;

	if( spike ) {
		/////////////// TODO: This is where we do the reset
	   neuron->V  = neuron->C;    // reset membrane voltage
		neuron->U += neuron->D;		// offset 2nd state variable
		//neuron->this_h = machine_timestep * SIMPLE_TQ_OFFSET; //REAL_CONST( 1.85 );  // simple threshold correction - next timestep (only) gets a bump
		}
	//else
		//neuron->this_h = machine_timestep;

	return spike;
}



/////////////////////////// Header file




#ifndef _IZH_CURR_NEURON_
#define _IZH_CURR_NEURON_


#include  "neuron/models/generic_neuron.h"

// TODO: need to get the Python definition in the same order
typedef struct neuron_t {

// nominally 'fixed' parameters
	REAL 		A;
	REAL 		B;
	REAL 		C;
	REAL		D;

// Variable-state parameters
	REAL 		V;
	REAL 		U;

// offset current [nA]
	REAL		I_offset;

// anything from here onwards is private to the c code (non neural parameters)
// current timestep - simple correction for threshold in beta version
	//REAL		this_h; // DAN: can ignore this


} neuron_t;


#endif   // include guard

