module generated_logic(input A, input B, input C, output logic_out);
    wire not_B;
    wire not_C;
    wire term_0;
    wire term_1;
    not g_not_B(not_B, B);
    not g_not_C(not_C, C);
    and g_term_0(term_0, A, not_B, C);
    and g_term_1(term_1, A, B, not_C);
    or g_output(logic_out, term_0, term_1);
endmodule
