module generated_logic(input A, input B, input C, output logic_out);
    wire term_0;
    wire term_1;
    and g_term_0(term_0, A, B);
    and g_term_1(term_1, A, C);
    or g_output(logic_out, term_0, term_1);
endmodule
