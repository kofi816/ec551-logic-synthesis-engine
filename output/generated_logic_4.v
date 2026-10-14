module generated_logic(input A, input B, input C, output logic_out);
    wire not_A;
    wire not_C;
    wire term_0;
    wire term_1;
    not g_not_A(not_A, A);
    not g_not_C(not_C, C);
    and g_term_0(term_0, not_A, B, C);
    and g_term_1(term_1, A, B, not_C);
    or g_output(logic_out, term_0, term_1);
endmodule
