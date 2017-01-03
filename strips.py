
import numpy as np
from model import GumbelAE

def dump_actions(transitions,path):
    # assert 2 == transitions.shape[0]
    ae = GumbelAE(path)
    ae.train(np.concatenate(transitions,axis=0),
             anneal_rate=0.0001,
             # epoch=400
    )

    orig, dest = transitions[0], transitions[1]
    orig_b, dest_b = ae.encode_binary(orig), ae.encode_binary(dest)
    
    actions = np.concatenate((orig_b, dest_b), axis=1)
    np.savetxt(ae.local("actions.csv"),actions,"%d")
    return actions


if __name__ == '__main__':
    import numpy.random as random
    def plot_grid(images,name="plan.png"):
        import matplotlib.pyplot as plt
        l = len(images)
        w = 10
        h = max(l//10,1)
        plt.figure(figsize=(20, h*2))
        for i,image in enumerate(images):
            # display original
            ax = plt.subplot(h,w,i+1)
            plt.imshow(image,interpolation='nearest',cmap='gray',)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        plt.savefig(name)

    def run(path, shape, transitions):
        actions = dump_actions(transitions, path)
        print actions[:3]
        ae = GumbelAE(path)
        xs = transitions[0][random.randint(0,transitions[0].shape[0],12)]
        zs = ae.encode_binary(xs)
        ys = ae.decode_binary(zs)
        bs = np.round(zs)
        bys = ae.decode_binary(bs)
        # 
        xs = xs.reshape(shape)
        zs = zs.reshape((-1,4,4))
        ys = ys.reshape(shape)
        bs = bs.reshape((-1,4,4))
        bys = bys.reshape(shape)
        images = []
        for x,z,y,b,by in zip(xs,zs,ys,bs,bys):
            images.append(x)
            images.append(z)
            images.append(y)
            images.append(b)
            images.append(by)
        plot_grid(images, ae.local("autoencoding.png"))

    import counter
    transitions = counter.transitions(n=1000)
    run("samples/counter_model/", (-1,28,28), transitions)
    
    import puzzle
    transitions = puzzle.transitions(2,2)
    transitions = np.repeat(transitions,100,axis=1)
    run("samples/puzzle_model/", (-1,6*2,5*2), transitions)
    
    import mnist_puzzle
    transitions = mnist_puzzle.transitions(2,2)
    transitions = np.repeat(transitions,100,axis=1)
    run("samples/mnist_puzzle_model/", (-1,28*2,28*2), transitions)

    import puzzle
    transitions = puzzle.transitions(3,2)
    transitions = np.repeat(transitions,100,axis=1)
    run("samples/puzzle3_model/", (-1,6*2,5*3), transitions)
    
