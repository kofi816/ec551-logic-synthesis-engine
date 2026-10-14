module generated_logic(input A, input B, output logic_out);
    wire term_0;
    wire term_1;
    buf g_term_0(term_0, A);
    buf g_term_1(term_1, B);
    or g_output(logic_out, term_0, term_1);
endmodule
