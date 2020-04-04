class BaseClass:
    num_base_class = 0

    def call_me(self, caller):
        print("Apel metoda din Base, caller= ", caller, "\n")
        self.num_base_class += 1

class LeftSubClass(BaseClass):
        num_left_class = 0

        def call_me(self, caller):
            print("Apel metoda din Left, caller= ", caller, "\n")
            BaseClass.call_me(self, "Left")
            self.num_base_class += 1


class RightSubClass(BaseClass):
    num_right_class = 0

    def call_me(self, caller):
        print("Apel metoda din Right, caller= ", caller, "\n")
        BaseClass.call_me(self, "Right")
        self.num_base_class += 1

class Subclass(LeftSubClass, RightSubClass):
    num_sub_class = 0

    def call_me(self, caller):
        print("Apel metoda din Sub, caller= ", caller, "\n")
        LeftSubClass.call_me(self, "Sub")
        RightSubClass.call_me(self, "Sub")
        self.num_sub_class += 1


if __name__ == '__main__':
    Subclass().call_me('__main__')

    #print(subclass.__mro__)
