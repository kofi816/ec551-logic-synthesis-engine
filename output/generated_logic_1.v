module generated_logic(input A, input B, output logic_out);
    wire not_A;
    wire not_B;
    wire term_0;
    wire term_1;
    not g_not_A(not_A, A);
    not g_not_B(not_B, B);
    and g_term_0(term_0, not_A, not_B);
    and g_term_1(term_1, A, B);
    or g_output(logic_out, term_0, term_1);
endmodule
