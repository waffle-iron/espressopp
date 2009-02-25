#include "VelocityVerlet.hpp"

#include "particles/Computer.hpp"
#include "pairs/ForceComputer.hpp"

using namespace espresso::integrator;
using namespace espresso::particles;
using namespace espresso::pairs;

typedef Storage::PropertyTraits<Real3D>::Reference RealArrayRef;

class StepA : public espresso::particles::Computer  {
   private:
     RealArrayRef pos;
     RealArrayRef vel;
     RealArrayRef force;

     real timeStep;
     real timeStepSqr;

   public:
      StepA(RealArrayRef _posRef, RealArrayRef _velRef,RealArrayRef _forceRef, real _timeStep):
          pos(_posRef), vel(_velRef), force(_forceRef),
          timeStep(_timeStep), timeStepSqr(_timeStep * _timeStep) {}

      // m = 1
      virtual void operator()(espresso::particles::Storage::reference pref) {
       pos[pref] = pos[pref] + vel[pref] * timeStep + 0.5 * force[pref] * timeStepSqr;
       
       force[pref] = 0.0;
      }

};

class StepB : public espresso::particles::Computer  {

  private:

    RealArrayRef vel;
    RealArrayRef force;

    real timeStep;

  public:

     StepB(RealArrayRef _velRef,RealArrayRef _forceRef, real _timeStep):

         vel(_velRef), force(_forceRef), timeStep(_timeStep) {}

     virtual void operator()(espresso::particles::Storage::reference pref) {

        vel[pref] = vel[pref] + 0.5 * force[pref] * timeStep;

     }

};

VelocityVerlet::VelocityVerlet(espresso::particles::Set* _particles, 
			       size_t _position, size_t _velocity, size_t _force):

     particles(_particles),
     storage(_particles->getStorage()),
     position(_position),
     velocity(_velocity),
     force(_force)

{}

void VelocityVerlet::addForce(espresso::interaction::Interaction *interaction, 
                              espresso::pairs::Set *pair) {
  
     interactions.push_back(interaction);
     pairs.push_back(pair);

}

void VelocityVerlet::run(int timesteps) {

    for (int i=0; i < timesteps; i++) {

       // Step A

       StepA stepA(storage->getProperty<Real3D>(position),
                   storage->getProperty<Real3D>(velocity),
                   storage->getProperty<Real3D>(force),
                   timeStep
                  );

       particles->foreach(stepA);

       // Force Loop 

       for (size_t k=0; k < interactions.size(); k++) {

           espresso::pairs::ForceComputer 
              forcecompute(storage->getProperty<Real3D>(force), *interactions[k]);

           pairs[k]->foreach(forcecompute);

       }

       // Step B

       StepB stepB(storage->getProperty<Real3D>(velocity),
                   storage->getProperty<Real3D>(force),
                   timeStep
                  );

       particles->foreach(stepB);

    }
}

VelocityVerlet::~VelocityVerlet() {}
