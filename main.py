#Create a base for doubly linked list. 

'''
The list will contain elements. Each element will have initialized with four values, first the value contained in it, second the previous element in the list, third the next element in the list. 
If it is a start or end element then the prev or next node will be none respectively. 
'''
class Element:
    def __init__(self, value, prev=None, next=None):
        self.value = value
        self.prev = prev
        self.next = next

class DLL:
    def __init__(self):
        self.length = 0
        self.first_value = None

    def add_at_start(self, value):
        if self.length == 0:
            self.first_value = Element(value)
        else:
            new_el = Element(value, next=self.first_value)
            self.first_value.prev = new_el
            self.first_value = new_el
        self.length += 1

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
                    break
                else:
                    current = current.next
    
    def add_at_pos(self, pos, value):
        pos = pos-1
        if pos >= self.length:
            self.add_at_end(value)
        else:
            for i in range(pos):
                if i == 0:
                    current = self.first_value
                elif i == pos-1:
                    current = current.next
                    new_el = Element(value, prev=current, next=current.next)
                    current.next = new_el
                    self.length += 1
                else:
                    current = current.next

    def remove_people(self, qty, pos):
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
                    subdll.print_dll()
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
            print(current.value)
    
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


if __name__ == "__main__":
    newdll = DLL()
    newdll.add_at_start("B")
    newdll.add_at_start("A")
    newdll.add_at_end("C")
    newdll.add_at_end("D")
    newdll.add_at_end("E")
    newdll.add_at_end("F")
    newdll.add_at_end("G")
    newdll.add_at_end("H")
    print(f"Length of the DLL: {newdll.length} ")
    newdll.print_dll()
    print("===NewLIst===")
    newdll.flip_order(4,3)
    print(f"Length of DLL : {newdll.length}")
    newdll.print_dll()
