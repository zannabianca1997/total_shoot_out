from Vec2d import Vec2d

class PhisicEngine:

    @staticmethod
    def Collided(A,B):

        #calcolo velocità relativa
        rv = B.speed - A.speed

        # calcolo la normale di impatto
        normal =  (B.position - A.position).normalized()

        #Calcolo componente lungo la velocità
        velLungoNormale = rv.dot(normal)

        #Ignora  se le velocità li allontanano
        if velLungoNormale > 0 :
            return

        # Calcola coeff. restituzione
        e = min( A.restitution, B.restitution)

        # Calcola modulo impulso
        j = -(e + 1) * velLungoNormale
        j /= A.inverseweight + B.inverseweight

        #Applica l'impulso
        impulso = normal * j
        A.takeimpulse(-impulso) #ovviamente opposto
        B.takeimpulse(impulso)



