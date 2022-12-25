class Element:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

class DLL:
    def __init__(self):
        self.length = 0
        self.first_value = None
        self.items = []

    def add_at_start(self, value):
        if self.length == 0:
            self.first_value = Element(value)
        else:
            new_el = Element(value, next=self.first_value)
            self.first_value.prev = new_el
            self.first_value = new_el
        self.length += 1
        self.items.append(self.first_value)

    def add_at_end(self, value):
        if self.length == 0:
            self.add_at_start(value)
        else:
            keep_running = True
            current = self.first_value
            while keep_running:
                if current.next == None:
                    new_el = Element(value, prev=current)
                    current.next = new_el
                    self.length += 1
                    self.items.append(self.first_value)
                    break
                else:
                    current = current.next
        
    
    def add_at_pos(self, pos, value):
        pos = pos-1
        if pos==0:
            self.add_at_start(value)
        elif pos == 1:
            new_el = Element(value, prev=self.first_value, next=self.first_value.next)
            self.first_value.next = new_el
            self.length += 1
        elif pos < self.length:
            for i in range(pos):
                if i == 0:
                    current = self.first_value
                elif i == pos-1:
                    current = current.next
                    new_el = Element(value, prev=current, next=current.next)
                    current.next = new_el
                    self.items.append(new_el)
                    self.length += 1
                else:
                    current = current.next
        else:
            self.add_at_end(value)

    def remove_people(self, qty, pos):
        pos = pos - 1
        if qty < 1:
            qty = 1
        if (pos >= self.length):
            raise IndexError("Position is larger than the length of DLL")
        elif pos == 0:
            for j in range(qty+1):
                if j==0:
                    current = self.first_value
                else:
                    current = current.next
            current.prev=None
            self.first_value = current
            self.length -= qty
        elif (pos+qty) > self.length:
            raise IndexError("Position+Quantity is larger than the length of DLL")
        elif (pos+qty) == self.length:
            for i in range(pos):
                if i==0:
                    current = self.first_value
                elif i == pos-1:
                    current = current.next
            current.next = None
            self.length -= qty

        else:
            for i in range(pos):
                if i == 0:
                    current = self.first_value
                elif i == pos-1:
                    current = current.next
                    
                    for j in range(qty+1):
                        if j == 0:
                            newnext = current.next
                        else:
                            newnext = newnext.next
                    newnext.prev = current
                    current.next = newnext
                    self.length -= qty
                else:
                    current = current.next

    def flip_order(self, qty, pos):
        pos = pos - 1
        if qty < 1:
            qty = 1
        if (pos >= self.length):
            raise IndexError("Position is larger than the length of DLL")
        elif (pos+qty) >= self.length:
            raise IndexError("Position+Quantity is larger than the length of DLL")
        else:
            for i in range(pos):
                if i == 0:
                    current = self.first_value
                elif i == pos-1:
                    current = current.next
                    for j in range(qty):
                        if j == 0:
                            newnext = current.next
                            subdll = DLL()
                            subdll.add_at_start(newnext.value)
                        else:
                            newnext = newnext.next
                            subdll.add_at_start(newnext.value)
                    # subdll.print_dll()
                    current.next = subdll.first_value
                    subdll.parse_dll().next = newnext.next
                    # newnext.prev = subdll.parse_dll()
                else:
                    current = current.next

    def print_dll(self):
        for i in range(self.length+1):
            if i==0:
                current = self.first_value
            else:
                if current.next is not None:
                    current = current.next
                else:
                    break
            print(current.value, end = " ")
    
    def parse_dll(self, pos=-1):
        if (pos == -1) or (pos>self.length):
            until = self.length
        else:
            until = pos
        for i in range(until):
            if i == 0:
                current_el = self.first_value
            else:
                if current_el.next is None:
                    current_el = current_el
                else:
                    current_el = current_el.next
        return current_el

def get_elements(dll:DLL):
    current = None
    keep_running = True
    # print("\n====DLL====\n")
    output = ""
    while keep_running:
        if current == None:
            current = dll.first_value
            if current == None:
                break
            else:
                output += current.value + " "
        else:
            current = current.next
            output += current.value + " "
        if current.next == None:
            keep_running = False
    return output

def output_text(inputfile:str, dll:DLL):
    with open(inputfile, "r") as f:
        data = f.readlines()
    outputfile = "outputPS14.txt"
    outputstr = ""
    for each_line in data:
        actions = each_line.strip().split("::")
        if actions[0] == "add_at_start":
            dll.add_at_start(actions[1])
            outputstr += get_elements(dll)
        elif actions[0] == "add_at_end":
            dll.add_at_end(actions[1])
            outputstr += get_elements(dll)

        elif actions[0] == "add_at_pos":
            dll.add_at_pos(int(actions[1]), actions[2])
            outputstr += get_elements(dll)

        elif actions[0] == "flip_order":
            dll.flip_order(int(actions[1]), int(actions[2]))
            outputstr += get_elements(dll)

        elif actions[0] == "remove_people":
            dll.remove_people(int(actions[1]), int(actions[2]))
            outputstr += get_elements(dll)
        outputstr += "\n\n"
    return outputstr
        

# def text_func(inputline, dll:DLL):
#     output = inputline.strip().split("::")
#     # print(f"Operation to be performed: {output}")
#     if output[0] == "add_at_start":
#         dll.add_at_start(output[1])
#         get_elements(dll)
#     elif output[0] == "add_at_end":
#         dll.add_at_end(output[1])
#         get_elements(dll)
#     elif output[0] == "add_at_pos":
#         dll.add_at_pos(int(output[1]), output[2])
#         get_elements(dll)
#     elif output[0] == "flip_order":
#         dll.flip_order(int(output[1]), int(output[2]))
#         get_elements(dll)
#     elif output[0] == "remove_people":
#         dll.remove_people(int(output[1]), int(output[2]))
#         get_elements(dll)
#     else:
#         print("Mistake in text format")

if __name__ == "__main__":

    # print(output_text("inputPS14.txt", dll=DLL()))
    with open("outputPS14.txt", "w") as f:
        f.write(output_text("inputPS14.txt", dll=DLL()))
    # with open("inputPS14.txt", "r") as f:
    #     data = f.readlines()
    
    # newdll = DLL()
    # for line in data:
    #     text_func(line, newdll)


