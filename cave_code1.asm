.cpu cortex-m0
.text
.global even
.global odd
.global sommig
.global add_func
.global cave_unit1
.global cave_unit2
.global cave_unit3
.global cave_unit4
.global cave_unit5
.global cave_unit6
.global cave_unit7
.global cave_unit8
.global cave_unit9
.global cave_unit10
.global cave_unit11
.global cave_unit12
.global cave_unit13
.global cave_unit14
.global cave_unit15
.global cave_unit16
.global cave_unit17
.global cave_unit18
.global cave_unit19

true:
	mov R0, #1
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
	ldr R0, [sp, #0]
	sub sp, sp, #4
	mov R1, #0
	cmp R0, R1
	beq even_a_eqooga_0_end
	mov R0, #0
	b even_end
even_a_eqooga_0_end:
	
	add sp, sp, #4
	ldr R0, [sp, #0]
	sub sp, sp, #4
	mov R1, #1
	sub R0, R1, R2
	
	add sp, sp, #0
	str R0, [sp, #0]
	sub sp, sp, #0
	
	add sp, sp, #0
	ldr R0, [sp, #0]
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
	ldr R0, [sp, #0]
	sub sp, sp, #4
	mov R1, #0
	cmp R0, R1
	beq odd_c_eqooga_0_end
	mov R0, #1
	b odd_end
odd_c_eqooga_0_end:
	
	add sp, sp, #4
	ldr R0, [sp, #0]
	sub sp, sp, #4
	mov R1, #1
	sub R0, R1, R2
	
	add sp, sp, #0
	str R0, [sp, #0]
	sub sp, sp, #0
	
	add sp, sp, #0
	ldr R0, [sp, #0]
	sub sp, sp, #0
	bl even
	b odd_end
odd_end:
	add sp, sp, #8
	pop {pc}

sommig:
	push {lr}
	sub sp, sp, #8
	
	add sp, sp, #4
	str R0, [sp, #0]
	sub sp, sp, #4
	
	add sp, sp, #0
	str R1, [sp, #0]
	sub sp, sp, #0
	
mov R0, #0
	
	add sp, sp, #0
	str R0, [sp, #0]
	sub sp, sp, #0
	
sommig_a_greqooga_1_condition:
	
	add sp, sp, #4
	ldr R0, [sp, #0]
	sub sp, sp, #4
	mov R1, #1
	cmp R0, R1
	blt sommig_a_greqooga_1_end
	
	add sp, sp, #0
	ldr R0, [sp, #0]
	sub sp, sp, #0
	
	add sp, sp, #4
	ldr R1, [sp, #0]
	sub sp, sp, #4
	add R0, R1, R2
	
	add sp, sp, #0
	str R0, [sp, #0]
	sub sp, sp, #0
	
	add sp, sp, #4
	ldr R0, [sp, #0]
	sub sp, sp, #4
	mov R1, #1
	sub R0, R1, R2
	
	add sp, sp, #4
	str R0, [sp, #0]
	sub sp, sp, #4
	b sommig_a_greqooga_1_condition
	
sommig_a_greqooga_1_end:
	
	add sp, sp, #0
	ldr R0, [sp, #0]
	sub sp, sp, #0
	b sommig_end
sommig_end:
	add sp, sp, #8
	pop {pc}

add_func:
	push {lr}
	sub sp, sp, #8
	
	add sp, sp, #4
	str R0, [sp, #0]
	sub sp, sp, #4
	
	add sp, sp, #0
	str R1, [sp, #0]
	sub sp, sp, #0
	

	add sp, sp, #4
	ldr R0, [sp, #0]
	sub sp, sp, #4
	
	add sp, sp, #0
	ldr R1, [sp, #0]
	sub sp, sp, #0
	add R0, R1, R2
	b add_func_end
add_func_end:
	add sp, sp, #8
	pop {pc}

cave_unit1:
	push {lr}
	sub sp, sp, #0
	mov R0, #2
	bl odd
	b cave_unit1_end
cave_unit1_end:
	add sp, sp, #0
	pop {pc}

cave_unit2:
	push {lr}
	sub sp, sp, #0
	mov R0, #2
	bl odd
	b cave_unit2_end
cave_unit2_end:
	add sp, sp, #0
	pop {pc}

cave_unit3:
	push {lr}
	sub sp, sp, #0
	mov R0, #21
	bl odd
	b cave_unit3_end
cave_unit3_end:
	add sp, sp, #0
	pop {pc}

cave_unit4:
	push {lr}
	sub sp, sp, #0
	mov R0, #20
	bl odd
	b cave_unit4_end
cave_unit4_end:
	add sp, sp, #0
	pop {pc}

cave_unit5:
	push {lr}
	sub sp, sp, #0
	mov R0, #1
	bl even
	b cave_unit5_end
cave_unit5_end:
	add sp, sp, #0
	pop {pc}

cave_unit6:
	push {lr}
	sub sp, sp, #0
	mov R0, #127
	bl even
	b cave_unit6_end
cave_unit6_end:
	add sp, sp, #0
	pop {pc}

cave_unit7:
	push {lr}
	sub sp, sp, #0
	mov R0, #21
	bl even
	b cave_unit7_end
cave_unit7_end:
	add sp, sp, #0
	pop {pc}

cave_unit8:
	push {lr}
	sub sp, sp, #0
	mov R0, #20
	bl even
	b cave_unit8_end
cave_unit8_end:
	add sp, sp, #0
	pop {pc}

cave_unit9:
	push {lr}
	sub sp, sp, #0
	mov R0, #2
	bl even
	b cave_unit9_end
cave_unit9_end:
	add sp, sp, #0
	pop {pc}

cave_unit10:
	push {lr}
	sub sp, sp, #0
	mov R0, #0
	bl odd
	b cave_unit10_end
cave_unit10_end:
	add sp, sp, #0
	pop {pc}

cave_unit11:
	push {lr}
	sub sp, sp, #0
	mov R0, #0
	bl even
	b cave_unit11_end
cave_unit11_end:
	add sp, sp, #0
	pop {pc}

cave_unit12:
	push {lr}
	sub sp, sp, #0
	mov R0, #5
	bl sommig
	b cave_unit12_end
cave_unit12_end:
	add sp, sp, #0
	pop {pc}

cave_unit13:
	push {lr}
	sub sp, sp, #0
	mov R0, #1
	bl sommig
	b cave_unit13_end
cave_unit13_end:
	add sp, sp, #0
	pop {pc}

cave_unit14:
	push {lr}
	sub sp, sp, #0
	mov R0, #1
	mov R1, #2
	add R0, R1, R2
	b cave_unit14_end
cave_unit14_end:
	add sp, sp, #0
	pop {pc}

cave_unit15:
	push {lr}
	sub sp, sp, #0
	mov R0, #1
	mov R1, #127
	add R0, R1, R2
	b cave_unit15_end
cave_unit15_end:
	add sp, sp, #0
	pop {pc}

cave_unit16:
	push {lr}
	sub sp, sp, #0
	mov R0, #1
	mov R1, #1
	sub R0, R1, R2
	b cave_unit16_end
cave_unit16_end:
	add sp, sp, #0
	pop {pc}

cave_unit17:
	push {lr}
	sub sp, sp, #0
	mov R0, #1
	mov R1, #2
	sub R0, R1, R2
	b cave_unit17_end
cave_unit17_end:
	add sp, sp, #0
	pop {pc}

cave_unit18:
	push {lr}
	sub sp, sp, #0
	mov R0, #1
	mov R1, #3
	mul R1, R1, R2
	mov R0, R1
	b cave_unit18_end
cave_unit18_end:
	add sp, sp, #0
	pop {pc}

cave_unit19:
	push {lr}
	sub sp, sp, #0
	mov R0, #3
	mov R1, #3
	mul R1, R1, R2
	mov R0, R1
	b cave_unit19_end
cave_unit19_end:
	add sp, sp, #0
	pop {pc}

