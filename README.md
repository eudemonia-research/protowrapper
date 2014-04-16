Protowrapper is a helper class that monkey patches protobuffer classes to assist validation.

It is best explained with an example:

    from protobuffer_pb2 import Address

    class Address(Protowrapper):

        def check_ip(self):
            return len(self.ip) == 4 || len(self.ip) == 16

        def check_port(self):
            return self.port > 0 and self.port < 1024

        def init(self):
            self.my_instance_variable = 0

        def print(self):
            print("ip:", self.ip, "port:", self.port)
            print("instance var", self.my_instance_variable)

And voila! Address is now a monkey patched protobuffer with those validation checks, initialization function, and other methods.
