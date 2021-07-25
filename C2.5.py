# C2.5. Итоговое практическое задание

player = input("Введите ваше имя: ")
print()
print(f"Приветствую вас {player}\n")
print("""Добро пожаловать в игру "Морской бой!"\n""")
print("Вы будите играть с ИИ\n")



field = [[" "] * 6 for i in range(6)]


def show_field():
    print()
    print("     1   2   3   4   5   6   ")
    print("   -------------------------")
    for i, row in enumerate(field):
        rows = f" {i+1} | {' | '.join(row)} | "
        print(rows)
        print("   ------------------------- ")
    print()


show_field()

# << GitHUB TEST >>
