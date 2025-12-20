import logging

from hud_controller.spec import ProblemSpec, PROBLEM_REGISTRY

logger = logging.getLogger(__name__)

# =============================================================================
# DESIGN TASKS - Implement from scratch
# =============================================================================

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="lifo_stack",
        description="""Implement a LIFO (Last-In-First-Out) stack with the following sub-modules:

**Module Requirements:**

1. **stack_pointer** - Stack pointer with push/pop control:
   - Inputs: clk, rst (synchronous reset), push, pop
   - Outputs: stack_addr[4:0], full, empty
   - 5-bit pointer (supports 17 entries: 0-16)
   - full when stack_addr == 16, empty when stack_addr == 0
   - push increments when not full, pop decrements when not empty

2. **stack_ram** - Stack memory:
   - Inputs: clk, stack_addr[4:0], stack_data_in[3:0], stack_we, stack_re
   - Output: stack_data_out[3:0]
   - 17-entry x 4-bit synchronous RAM
   - Write on rising edge when stack_we=1
   - Read outputs data when stack_re=1, else 0

3. **stack_data_mux** - Input data multiplexer:
   - Inputs: data_in[3:0], pc_in[3:0], stack_mux_sel
   - Output: stack_mux_out[3:0]
   - Selects data_in when stack_mux_sel=1, else pc_in

4. **lifo_stack** (top-level) - Connects all submodules:
   - Integrates stack_pointer, stack_ram, and stack_data_mux
   - Top-level interface matches specification

Implement all TODO sections in sources/lifo_stack.v to pass the tests.
""",
        difficulty="medium",
        base="lifo_stack_baseline",
        test="lifo_stack_test",
        golden="lifo_stack_golden",
        test_files=["tests/test_lifo_stack_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="microcode_arithmetic",
        description="""Implement a microcode arithmetic unit that forms the ALU datapath with auxiliary register storage, operand multiplexing, and 4-bit carry-lookahead adder logic.

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

4. **a_mux** - Operand A multiplexer:
   - Selects operand A from: register_data, data_in, or zero
   - Controlled by a_mux_sel[1:0]

5. **b_mux** - Operand B multiplexer:
   - Selects operand B from: pc_data, stack_data, zero, or register_data
   - Controlled by b_mux_sel[1:0]

6. **microcode_arithmetic** (top-level) - Connects all submodules

Implement all TODO sections in sources/microcode_arithmetic.v to pass the tests.
""",
        difficulty="medium",
        base="microcode_arithmetic_baseline",
        test="microcode_arithmetic_test",
        golden="microcode_arithmetic_golden",
        test_files=["tests/test_microcode_arithmetic_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="program_counter",
        description="""Implement a program counter module for the microcode sequencer.

The program counter should support:
- Synchronous reset
- Increment operation
- Load from external value
- Hold current value

See sources/program_counter.v for the interface and implement the TODO sections.
""",
        difficulty="easy",
        base="program_counter_baseline",
        test="program_counter_test",
        golden="program_counter_golden",
        test_files=["tests/test_program_counter_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="instruction_decoder_0",
        description="""Implement instruction decoder variant 0 for the microcode sequencer.

The instruction decoder decodes instruction opcodes into control signals for the datapath.

See sources/instruction_decoder_0.v for the interface and docs/Specification.md for details.
Implement all TODO sections to pass the tests.
""",
        difficulty="medium",
        base="instruction_decoder_0_baseline",
        test="instruction_decoder_0_test",
        golden="instruction_decoder_0_golden",
        test_files=["tests/test_instruction_decoder_0_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="instruction_decoder_1",
        description="""Implement instruction decoder variant 1 for the microcode sequencer.

See sources/instruction_decoder_1.v for the interface and docs/Specification.md for details.
Implement all TODO sections to pass the tests.
""",
        difficulty="medium",
        base="instruction_decoder_1_baseline",
        test="instruction_decoder_1_test",
        golden="instruction_decoder_1_golden",
        test_files=["tests/test_instruction_decoder_1_hidden.py"],
    )
)

# =============================================================================
# BUG FIX TASKS - Debug existing code
# =============================================================================

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="instruction_decoder_1_bug_fix",
        description="""Debug the instruction decoder 1 module.

The RTL module for the microcode sequencer's instruction decoder is failing simulation.
The simulation fails at the testcase that generates random combinations of inputs.

Debug and fix the RTL file at sources/instruction_decoder_1.v based on the specification
available at docs/Specification.md.

Find and fix the bug(s) to pass all tests.
""",
        difficulty="medium",
        base="instruction_decoder_1_bug_fix_baseline",
        test="instruction_decoder_1_bug_fix_test",
        golden="instruction_decoder_1_bug_fix_golden",
        test_files=["tests/test_instruction_decoder_1_hidden.py"],
    )
)

PROBLEM_REGISTRY.append(
    ProblemSpec(
        id="instruction_decoder_2_bug_fix",
        description="""Debug the instruction decoder 2 module.

The RTL module is failing simulation. Debug and fix the RTL file at 
sources/instruction_decoder_2.v based on the specification at docs/Specification.md.
""",
        difficulty="medium",
        base="instruction_decoder_2_bug_fix_baseline",
        test="instruction_decoder_2_bug_fix_test",
        golden="instruction_decoder_2_bug_fix_golden",
        test_files=["tests/test_instruction_decoder_2_hidden.py"],
    )
)
