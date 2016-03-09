from retino.model import Model


def generate_model(model_number, number_of_iterations):
    model = Model(name=str(model_number))
    model.iterate()


if __name__ == '__main__':

    for i in range(4):
        p = Process(target=generate_model, args=(i, 100))
        p.start()
        print("Started P", i, "for", targets[i])
