.cpu cortex-m0
.text
.global even
.global odd
.global asm_main

true:
	ldr R0, =1
	mov pc, lr

even:
	push {lr}
	sub sp, sp, #8
	add sp, sp, #4
	str R0, [sp, #0]
	sub sp, sp, #4
	add sp, sp, #0
	str R1, [sp, #0]
	sub sp, sp, #0
	
	add sp, sp, #4
	ldr R1, [sp, #0]
	sub sp, sp, #4
	ldr R2, =0
	add R3, pc, #24
	mov lr, R3
	cmp R1, R2
	beq true
	ldr R0, =0
	cmp R0, #0
	beq even_a_eqooga_0_end
	ldr R0, =0
	b even_end
even_a_eqooga_0_end:
	add sp, sp, #4
	ldr R1, [sp, #0]
	sub sp, sp, #4
	ldr R2, =1
	sub R0, R1, R2
	add sp, sp, #0
	str R0, [sp, #0]
	sub sp, sp, #0
	bl odd
	b even_end
even_end:
	add sp, sp, #8
	pop {pc}

odd:
	push {lr}
	sub sp, sp, #8
	add sp, sp, #4
	str R0, [sp, #0]
	sub sp, sp, #4
	add sp, sp, #0
	str R1, [sp, #0]
	sub sp, sp, #0
	
	add sp, sp, #4
	ldr R1, [sp, #0]
	sub sp, sp, #4
	ldr R2, =0
	add R3, pc, #24
	mov lr, R3
	cmp R1, R2
	beq true
	ldr R0, =0
	cmp R0, #0
	beq odd_c_eqooga_0_end
	ldr R0, =1
	b odd_end
odd_c_eqooga_0_end:
	add sp, sp, #4
	ldr R1, [sp, #0]
	sub sp, sp, #4
	ldr R2, =1
	sub R0, R1, R2
	add sp, sp, #0
	str R0, [sp, #0]
	sub sp, sp, #0
	bl even
	b odd_end
odd_end:
	add sp, sp, #8
	pop {pc}

asm_main:
	push {lr}
	sub sp, sp, #0
	bl odd
	b asm_main_end
asm_main_end:
	add sp, sp, #0
	pop {pc}

