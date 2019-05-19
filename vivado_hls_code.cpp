#include <ap_fixed.h>
#include <ap_int.h>
#include <stdint.h>
#include <assert.h>

typedef ap_uint<8> pixel_type;
typedef ap_int<8> pixel_type_s;
typedef ap_uint<96> u96b;
typedef ap_uint<32> word_32;
typedef ap_ufixed<8,0, AP_RND, AP_SAT> comp_type;
typedef ap_fixed<10,2, AP_RND, AP_SAT> coeff_type;

struct pixel_data {
  pixel_type blue;
  pixel_type green;
  pixel_type red;
};

void template_filter(volatile uint32_t* in_data, volatile uint32_t* out_data, int w, int h, int* sqrState, int hstartPt, int wstartPt, int* writesqrS) {
  #pragma HLS INTERFACE s_axilite port=return
  #pragma HLS INTERFACE s_axilite port=w
  #pragma HLS INTERFACE s_axilite port=h
  #pragma HLS INTERFACE s_axilite port=hstartPt
  #pragma HLS INTERFACE s_axilite port=wstartPt
  #pragma HLS INTERFACE s_axilite port=sqrState
  #pragma HLS INTERFACE s_axilite port=writesqrS

  #pragma HLS INTERFACE m_axi depth=2073600 port=in_data offset=slave // This will NOT work for resolutions higher than 1080p
  #pragma HLS INTERFACE m_axi depth=2073600 port=out_data offset=slave

  if(*sqrState==0) {
    out:for(int i=0; i<h; ++i) {
      inpipe:for(int j=0; j<w; ++j) {
        unsigned int current = *in_data++;
        unsigned char in_r=current & 0xFF;
        unsigned char in_g=(current>>8) & 0xFF;
        unsigned char in_b=(current>>16) & 0xFF;
        unsigned char out_r=0;
        unsigned char out_g=0;
        unsigned char out_b=0;
        unsigned int output = current;

        if((hstartPt-i<0 && hstartPt-i>-200) && (wstartPt-j<0 && wstartPt-j>-200)) {
          output=0xFF69B4;
        }
        *out_data++ = output;
      }
    }
    *writesqrS = 1;
  }
  else if(*sqrState==1) {
	*writesqrS=1;
  secout:  for(int i=0; i<h; ++i) {
      secpipe:for(int j=0; j<w; ++j) {
        unsigned int current = *in_data++;
        unsigned char in_r=current & 0xFF;
        unsigned char in_g=(current>>8) & 0xFF;
        unsigned char in_b=(current>>16) & 0xFF;
        unsigned char out_r=0;
        unsigned char out_g=0;
        unsigned char out_b=0;
        unsigned int output = current;
        if((hstartPt-i<0 && hstartPt-i>-200) && (wstartPt-j<0 && wstartPt-j>-200)) {
          output=0xFF69B4;
        }
        if((in_g - in_r > 25) && (in_g - in_b > 25)) { //in_r+in_b-12<in_g
          if((hstartPt-i<0 && hstartPt-i>-200) && (wstartPt-j<0 && wstartPt-j>-200)) {
            *writesqrS=0;
            output=0x000000;
          }
          else{
            output=0xFFFFFF;
          }
        }
        *out_data++ = output;
      }
    }
  }
}
