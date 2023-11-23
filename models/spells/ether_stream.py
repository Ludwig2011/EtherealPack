from CommonContent import SimpleRangedAttack
from Level import *
from mods.EtherealPack.models.buffs.etherealness_buff import EtherealnessBuff
from mods.EtherealPack.tags.Ethereal import Ethereal

def ÄtherImp():
	unit = Unit()
	unit.sprite.color = Color(1,121,111)
	unit.asset_name = os.path.join("..", "..", "mods", "EtherealPack", "ether_hydra")
	unit.name = "Äther Imp"
	unit.resists[Ethereal] = 100
	unit.resists[Tags.Physical] = 75
	unit.resists[Tags.Dark] = 50
	unit.resists[Tags.Holy] = 50
	unit.resists[Tags.Arcane] = -100
	unit.flying = True
	unit.shields = 1
	unit.max_hp = 7
	unit.spells.append(SimpleRangedAttack("Äther Bolt",7,Ethereal,5,buff=EtherealnessBuff,buff_duration=3))
	return unit

class EtherStream(Spell):

	def on_init(self):
		self.requires_los = False
		self.range = 99
		self.name = "Äther Stream"
		self.max_charges = 4
		self.asset = ['EtherealPack', 'ether_stream']
		self.tags = [Ethereal, Tags.Sorcery, Tags.Translocation]
		self.level = 3
		self.num_summons = 0
		self.minion_health = 0
		self.minion_damage = 0

		self.upgrades['max_charges'] = (3, 2)
		self.upgrades['num_summons'] = (3, 3, "Imp Friends", "Summon Äther Imps at the beginning of the stream")

	def get_description(self):
		return ("Jump into an Äther Stream found next to an [Äther:äthereal] or [ätherealiesed:äthereal] unit and leave next to one aswell"
			    "Teleport to any tile adjacent to an [Äther:äthereal] or [ätherealiesed:äthereal] unit.\n"
				"Can only be cast while adjacent to an [Äther:äthereal] or [ätherealiesed:äthereal] unit.").format(**self.fmt_dict())

	def can_cast(self, x, y):
		
		if not self.caster.level.can_stand(x, y, self.caster):
			return False

		for center in [self.caster, Point(x, y)]:
			next_to_äther = False
			for p in self.caster.level.get_points_in_ball(center.x, center.y, 1.5, diag=True):
				unit = self.caster.level.tiles[p.x][p.y].unit
				if unit and (unit.has_buff(EtherealnessBuff) or Ethereal in unit.tags):
					next_to_äther = True
					break
			if not next_to_äther:
				return False
		return Spell.can_cast(self, x, y)

	def cast_instant(self, x, y):

		old_loc = Point(self.caster.x, self.caster.y)
		self.caster.level.act_move(self.caster, x, y, teleport=True)

		for point in [old_loc, self.caster]:
			for i in range(self.get_stat('num_summons')):
				p = self.caster.level.get_summon_point(point.x, point.y, sort_dist=False)
				if p:
					imp = ÄtherImp()
					imp.max_hp += self.get_stat('minion_health')
					imp.spells[0].damage += self.get_stat('minion_damage')
					imp.team = self.caster.team
					self.summon(imp, p)