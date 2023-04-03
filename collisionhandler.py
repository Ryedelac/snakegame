import events as ev


def handlecollisions(world):
    #print("yer")
    for i in range(len(world.entities)):
            for j in range(i, len(world.entities)):
                if world.entities[i].collides_with(world.entities[j]):
                    world.message_queue.append(ev.EntityCollisionMessage(world.entities[i], world.entities[j]))
                    world.message_queue.append(ev.EntityCollisionMessage(world.entities[j], world.entities[i]))