.text
.global even
.global odd
.global main

true:
	ldr R0, =1
	mov pc, lr

even:
	push {lr}
	sub sp, sp, #8
	add sp, sp, #8
	str R0, [sp, #0]
	sub sp, sp, #8
	add sp, sp, #4
	str R1, [sp, #0]
	sub sp, sp, #4
	
	add sp, sp, #8
	ldr R1, [sp, #0]
	sub sp, sp, #8
	ldr R2, =0
	add R3, pc, #6
	mov lr, R3
	cmp R1, R2
	beq true
	ldr R0, =0
	cmp R0, #0
	beq even_a_eqooga_0_end
	ldr R0, =0
	b even_end
even_a_eqooga_0_end:
	add sp, sp, #8
	ldr R1, [sp, #0]
	sub sp, sp, #8
	ldr R2, =1
	sub R0, R1, R2
	add sp, sp, #4
	str R0, [sp, #0]
	sub sp, sp, #4
	bl odd
	b even_end
even_end:
	add sp, sp, #8
	pop {pc}

odd:
	push {lr}
	sub sp, sp, #8
	add sp, sp, #8
	str R0, [sp, #0]
	sub sp, sp, #8
	add sp, sp, #4
	str R1, [sp, #0]
	sub sp, sp, #4
	
	add sp, sp, #8
	ldr R1, [sp, #0]
	sub sp, sp, #8
	ldr R2, =0
	add R3, pc, #6
	mov lr, R3
	cmp R1, R2
	beq true
	ldr R0, =0
	cmp R0, #0
	beq odd_c_eqooga_0_end
	ldr R0, =1
	b odd_end
odd_c_eqooga_0_end:
	add sp, sp, #8
	ldr R1, [sp, #0]
	sub sp, sp, #8
	ldr R2, =1
	sub R0, R1, R2
	add sp, sp, #4
	str R0, [sp, #0]
	sub sp, sp, #4
	bl even
	b odd_end
odd_end:
	add sp, sp, #8
	pop {pc}

main:
	push {lr}
	sub sp, sp, #0
	bl odd
	b main_end
main_end:
	add sp, sp, #0
	pop {pc}

