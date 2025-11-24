import logging

from hud_controller.spec import ProblemSpec, PROBLEM_REGISTRY

logger = logging.getLogger(__name__)


PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="simple_counter",
        description="""Please implement a simple synchronous counter that with reset, enable, and load functionality.
Inputs:
clk - Clock signal (triggers on rising edge)
rst - Synchronous reset signal
ena - Enable signal (allows counting)
set - Load signal (sets counter to a specific value)
din - 8-bit data input (value to load when set is high)
Output:
counter - 8-bit counter value        
        
""",
        difficulty="easy",
        base="simple_counter_baseline",
        test="simple_counter_test",
        golden="simple_counter_golden",
        test_files=["tests/test_simple_counter_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="simple_dff",
        description="""Please implement a simple digital flip-flop with a clock input and a data input. 
The output should be the same as the data input on the rising edge of the clock.

Inputs:
clk - Clock signal (triggers on rising edge)
d - Data input
Output:
q - Output value      
""",
        difficulty="easy",
        base="simple_dff_baseline",
        test="simple_dff_test",
        golden="simple_dff_golden",
        test_files=["tests/test_simple_dff_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="rc5_ca_keygen",
        description="""Complete the given partial Systemverilog RTL code based on the specification /workdir/docs/Specification.md. The RTL code should be synthesizable. The key generation should be present in a separate module CA_8bit.sv that has to be instantiated in the module rc5_enc_16bit.sv.

Key generation

Key generation uses an 8‑bit one‑dimensional binary Cellular Automata (CA) with Rules 90 and 150. Cellular Automata is a Pseudo Random Number Generator (PRNG) approach based on selected rules. Every CA logical circuit can be constructed with D Flip-Flops (Register) and XOR gates. Construction of every CA register is based on the logical relationship of each flip-flop to its two nearest neighbors. These relationships are referred to as "rules" and two of the most popular rules are R90 and R150. CA based PRNG constructed with correct combination of these rules between the registers can yield maximal length sequence of 2n-1 random numbers, where n represents the number of registers in CA logical circuit.

Let x(i),x(i-1) and x(i+1) be the present register, previous register and next register in a n-bit CA. The rules R90 and R150 can be described as:

Rule 90: x(i) = x(i-1) XOR x(i+1)
Rule 150: x(i) = x(i-1) XOR x(i) XOR x(i+1)

Other considerations for CA based key generation:

Boundary handling: when a neighbor is out of range (for the MSB/LSB), treat that neighbor as 0.
For the 8-bit CA required for key generation, apply rules per bit, from MSB (bit 7) to LSB (bit 0), in this order: R90, R90, R150, R90, R150, R90, R150, R90.
On active‑LOW reset, initialize the CA_out to 8'hFF. On each rising clock edge, update all 8 bits of CA_out simultaneously to produce the next 8‑bit key (one key per cycle).
Generate the required number of 8‑bit keys for two RC5 rounds as specified by the task (the FSM's first state is responsible for this).

The interface of the CA_8bit module is given below:
clock - 1-bit Clock input. CA generates 8-bit key on rising edge of this clock
reset - 1-bit asynchronous active LOW reset input.
CA_seed[7:0] - 8-bit CA seed
CA_out[7:0] - 8-bit CA output

Partial RTL code

```
`timescale 1ns/1ps
module rc5_enc_16bit (input clock,//Positive edge-triggered clock
                                     input reset,//Asynchronous active low reset
			     input enc_start, //When HIGH, encryption begins
			     input [15:0]p, //Plaintext input
			     output reg [15:0]c, //Ciphertext output
			     output reg enc_done); //When HIGH, indicates the stable ciphertext output
	//Insert internal signal declarations
	
	//Instantiate the Key generation module based on cellular automata
	
	//Insert FSM to handle two rounds of encryption. 
	
endmodule
```

**Important**: This environment uses Icarus Verilog for testing. Avoid using SystemVerilog Assertion (SVA) property/sequence syntax if adding assertions.

## Hints
- **Key Generation**: The number of keys required for two rounds have to be generated in the first state of FSM
""",
        difficulty="hard",
        base="rc5_ca_keygen_baseline",
        test="rc5_ca_keygen_test",
        golden="rc5_ca_keygen_golden",
        test_files=["tests/test_rc5_enc_16bit_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="rc5_enc_dec_param",
        description="""Spec-to-rtl task:

Title: RC5 encryption & decryption core (parametric)

Implement a synthesizable SystemVerilog module rc5_enc_dec_param that performs RC5 encryption and decryption per docs/Specification.md.

Objective:
Parameterized RC5 core with start/done handshakes for both encryption and decryption.
Internal, seed-driven key generation compatible with RC5 S-box usage.

Interface:
Inputs: clock, reset (async active-LOW), enc_start, dec_start, p_in[w-1:0], c_in[w-1:0], lfsr_seed_enc[7:0], lfsr_seed_dec[7:0]
Outputs: c_out[w-1:0], p_out[w-1:0], enc_done, dec_done
Parameters: w=16, r=3

You need to implement TWO files:
1. sources/rc5_enc_dec_param.sv - Main RC5 encryption/decryption module
2. sources/lfsr_8bit.sv - 8-bit LFSR for key generation

See docs/Specification.md for complete algorithm details.
See hints.txt for implementation guidance.

For testing purposes, use the following timing directive as the first line of your rc5_enc_dec_param.sv file: `timescale 1ns/1ps
""",
        difficulty="hard",
        base="rc5_enc_dec_param_baseline",
        test="rc5_enc_dec_param_test",
        golden="rc5_enc_dec_param_golden",
        test_files=["tests/test_rc5_enc_dec_param_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="microcode_arithmetic",
        description="""Implement a microcode arithmetic unit that forms the ALU datapath with auxiliary register storage, operand multiplexing, and 4-bit carry-lookahead adder logic.

The microcode_arithmetic block enables micro-operations like addition or pass-through and is composed of multiple sub-modules that need to be implemented.

**Module Requirements:**

1. **full_adder** - 4-bit carry-lookahead adder with:
   - Inputs: a_in[3:0], b_in[3:0], cen (carry enable), c_in (carry in)
   - Outputs: y_out[3:0] (sum/XOR based on cen), c_out (carry out), g_out (group generate), p_out (group propagate)
   - When cen=0: y_out = a_in XOR b_in (XOR mode)
   - When cen=1: y_out = a_in + b_in + c_in (full addition with CLA)

2. **aux_reg_mux** - Auxiliary register input multiplexer:
   - Selects between reg1_in (fa_in) and reg2_in (d_in) based on rsel
   - Controlled by re (register enable)

3. **aux_reg** - Auxiliary register with clock:
   - 4-bit register with enable control (rce) and output enable (re)
   - Stores intermediate values for multi-cycle operations

4. **a_mux** - Operand A multiplexer:
   - Selects operand A from: register_data, data_in, or zero
   - Controlled by a_mux_sel[1:0]

5. **b_mux** - Operand B multiplexer:
   - Selects operand B from: pc_data, stack_data, zero, or register_data
   - Controlled by b_mux_sel[1:0]

6. **microcode_arithmetic** (top-level) - Connects all submodules:
   - Integrates the adder, muxes, and register
   - Output tri-state control via oen and oe (active-low output enable)
   - Routes carry/generate/propagate signals from adder to top-level outputs

**Implementation Tips:**
- Use proper Verilog syntax (wire/reg declarations)
- Implement CLA (carry-lookahead) logic for full_adder with proper P and G signals
- Handle tri-state output correctly: d_out should be Z when oen=0 or oe=1
- All sub-modules are already declared with correct interfaces in sources/microcode_arithmetic.v

**Testing:**
The hidden tests verify:
- Basic addition paths through the ALU
- XOR mode (cen=0) operation
- Tri-state output control
- Auxiliary register write/read operations
- Randomized test scenarios

Implement all the TODO sections in sources/microcode_arithmetic.v to pass the tests.
""",
        difficulty="medium",
        base="microcode_arithmetic_baseline",
        test="microcode_arithmetic_test",
        golden="microcode_arithmetic_golden",
        test_files=["tests/test_microcode_arithmetic_hidden.py"],
    )
)
