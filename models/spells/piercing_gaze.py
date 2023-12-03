from CommonContent import PetrifyBuff, Poison
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal


class PiercingGaze(Spell): # cone?

    def on_init(self):
        self.name = "Piercing Gaze"
        self.asset = ['EtherealPack', 'piercing_gaze']

        self.range = 99
        self.max_charges = 7
        self.duration = 7
        self.damage = 1
        self.requires_los = True
        self.angle = math.pi / 5

        self.tags = [Ethereal, Tags.Nature, Tags.Sorcery]
        self.level = 3
        self.upgrades['requires_los'] = (-1, 2)
        self.upgrades['duration'] = (7, 2)
        #self.upgrades['damage'] = (6, 4)
        self.upgrades['unnerving_gaze'] = (1, 2, "Unnerving Gaze", "Ätherealies enemies aswell")
        self.upgrades['shocking_gaze'] = (1, 4, "Shocking Gaze", "Petrify affected enemies for 2 turns")



    def get_description(self):
        return ("[Poison:poison] all enemies in a cone for [{duration}_turns:duration].\n"
                "Deals [{damage}_äthereal:äthereal] and [{damage}_physical:physical] damage to affected enemies.").format(**self.fmt_dict())
    
    def get_impacted_tiles(self, x, y):
        return [p for stage in Cone(self.caster, self.get_stat('range'), BurstConeParams(Point(x,y), self.get_stat('angle')), requires_los=self.get_stat('requires_los')) for p in stage]

    def cast(self, x, y):
        units = []
        for stage in Cone(self.caster, self.get_stat('range'), BurstConeParams(Point(x,y), self.get_stat('angle')), requires_los=self.get_stat('requires_los')):
            for p in stage:
                unit = self.caster.level.get_unit_at(p.x,p.y)
                if unit:
                    units.append(unit)
        targets = [u for u in units if u != self.caster and are_hostile(u, self.caster)]
        #targets = sorted(targets, key=lambda u: distance(u, self.caster))

        for target in targets:
            target.apply_buff(Poison(), self.get_stat('duration'))
            target.deal_damage(self.get_stat('damage'), Tags.Physical, self)
            target.deal_damage(self.get_stat('damage'), Ethereal, self)
            if target.cur_hp > 0: 
                if self.get_stat('unnerving_gaze'):
                    target.apply_buff(EtherealnessBuff(), self.get_stat('duration'))
                if self.get_stat('shocking_gaze'):
                    target.apply_buff(PetrifyBuff(), 2)
            yield

class Cone():
	# A sequencing tool for explosions and explosion like phenomena
	def __init__(self, caster, radius, burst_cone_params=None, expand_diagonals=False, requires_los=True):
		self.caster = caster
		self.radius = radius
		self.burst_cone_params = burst_cone_params

		# Auto expand diagonals in cones, they dont work otherwise.
		self.expand_diagonals = expand_diagonals if not burst_cone_params else True
		self.requires_los = requires_los

	def is_in_burst(self, p):
		if self.requires_los and not self.caster.level.can_see(p.x, p.y, self.caster.x, self.caster.y):
			return False

		dist = distance(p, self.caster)
		if dist > self.radius:
			return False

		angle = abs(get_min_angle(self.caster.x, 
								  self.caster.y, 
								  self.burst_cone_params.target.x, 
								  self.burst_cone_params.target.y, 
								  p.x, 
								  p.y)) 

		return angle <= self.burst_cone_params.angle

	def __iter__(self):

		already_exploded = set([self.caster])
		last_stage = set([self.caster])

		# start with the center point obviously
		if not self.burst_cone_params:
			yield set([self.caster])

		for i in range(self.radius):
			next_stage = set()

			for point in last_stage:
				ball_radius = 1.5 if self.expand_diagonals else 1.1
				next_stage.update(self.caster.level.get_points_in_ball(point.x, point.y, ball_radius, diag=self.expand_diagonals))

			next_stage.difference_update(already_exploded)

			if self.burst_cone_params is not None:
				next_stage = [p for p in next_stage if self.is_in_burst(p)]

			already_exploded.update(next_stage)
			yield next_stage
			last_stage = next_stage