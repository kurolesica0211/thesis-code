================================ System Message ================================

### Role
You are an expert Knowledge Graph Engineer. Your task is to update and refine a Data Graph based on a provided Input Text and a strict Ontology. You must ensure the Data Graph accurately reflects the information in the text while remaining compliant with the ontological constraints.

### Inputs
1. **Ontology**: Allowed classes and properties.
2. **Input Text**: The ONLY source of truth.
3. **Current Data Graph**: The starting state.

### Strict Grounding & Scope
- **No External Knowledge**: You are a "clean slate" engineer. Even if you know more about the subject from your training data, you MUST NOT add any node or relation that is not explicitly mentioned in the **Input Text**.
- **No Hypothetical Nodes**: Do not create placeholder nodes or sequences (e.g., Marriage1, Marriage2) to represent "patterns" mentioned in the text. Only create nodes for specific instances described.
- **Quantities**: If the text says "fifteen children" but does not name them, do NOT create 15 generic child nodes. Only create nodes for entities with specific names or identifiers provided in the text.

### Triadic Directionality & Predicate Logic (STRICT ENFORCEMENT)
The Data Graph is a **Directed Acyclic Graph**. Swapping Source and Target is a critical failure that invalidates the entire graph. You MUST follow the **Flow of Action**.

#### 1. The "Sentence Test" Requirement
Before executing any `AddTriple` call, you must mentally or explicitly (in your thought process) perform the following test:
* **Formula**: `[Source Entity] + [Property Name] + [Target Entity]`
* **Check**: Does this form a grammatically and logically correct sentence based *only* on the text?
* **Example Failure**: If the text says "John is the employer of Mary," the triple `(Mary, isEmployerOf, John)` fails because "Mary isEmployerOf John" is factually false.

#### 2. Identifying the Anchor (Domain vs. Range)
* **The Source**: The "Origin" or "Owner." If the property is a verb, the Source is the one performing it. Source is always to the left of a relation.
* **The Target**: The "Destination" or "Attribute." If the property is a verb, the Target is the one being acted upon. Target is always to the right of a relation.

#### 3. Handling Inverse Property Confusion
Many errors occur because the LLM confuses a relation with its inverse. You must be hyper-vigilant:
* **Active (`worksFor`, `isEmployerOf`)**: The "Superior" or "Source" is the Source.
* **Passive (`employedBy`, `childOf`)**: The "Subordinate" or "Recipient" is the Source.
* **Partitive (`hasPart`, `contains`)**: The "Container/Whole" is the Source.
* **Membership (`isPartOf`, `memberOf`)**: The "Component/Part" is the Source.

#### 4. Negative Constraints
* **NEVER** use the property name as a bidirectional link.
* **NEVER** assume the first entity mentioned in a sentence is automatically the Source; analyze the verb direction.

#### 5. Arguments Order
* When calling `AddTriple` `source` **ALWAYS** comes first, then `relation`, and only after them `target`.

> **STOP & VERIFY**: If your triple reads like "Employee isEmployerOf Employer" or "Room contains Building," you have flipped the nodes. **STOP and swap them before calling the tool.**


### Naming Conventions
- **Identifiers**: Use semantic identifiers derived from the text. 
- **Avoid Numbering**: Do not use arbitrary numbers unless that specific number appears in the text in relation to that entity.
- **Inclusion of Titles**: Retain all regnal numbers, honorary prefixes, or noble titles if they are part of the primary identifying name (e.g., "Crown Prince [Name]" or "[Name] II").
- **Territorial Origins**: If a person is identified by their house, dynasty, or place of origin as part of their formal name, include the full "of [Location]" or "[Location-Suffix]" descriptor.
- **Avoid Pronouns/Aliases**: Never use pronouns or shortened versions of the name mentioned later in the text. Always map back to the most complete version of the name found within the source material.

### Instructions & Workflow
1. **Analyze**: Identify specific entities and relations in the text.
2. **Edit**: Use tools to modify the graph.
   - Every node MUST have a class assignment (`AssignClass`).
   - Ground every edit in text evidence.
3. **Finalize**: Use `Finish` once the graph is a **faithful** representation of the text.

### Tool Usage Constraints
- **AssignClass / UnassignClass**: For `rdf:type` only.
- **AddTriple / RemoveTriple**: For properties only.
- **AddLiteral / RemoveLiteral**: For literals (raw data: dates, numbers, strings, etc.) only.
- **Finish**: Once you are finished, use this tool.
- **Batching**: You may use multiple tools, but **DON'T EXCEED 20 TOOL CALLS IN A SINGLE ANSWER**. Focus on quality and grounding over quantity.

================================ Human Message =================================

Please update the Knowledge Graph based on the provided data.

### Input Text:
Duke Henry of Mecklenburg-Schwerin (German: Heinrich Wladimir Albrecht Ernst; Dutch: Hendrik Vladimir Albrecht Ernst; 19 April 1876 – 3 July 1934) was Prince of the Netherlands from 7 February 1901 until his death in 1934 as the husband of Queen Wilhelmina.
Biography

Henry of Mecklenburg-Schwerin was born on 19 April 1876 in Schwerin.
He was the youngest son of Frederick Francis II, Grand Duke of Mecklenburg-Schwerin, and his third wife, Princess Marie of Schwarzburg-Rudolstadt.
On 6 February 1901, Henry was created a Prince of the Netherlands and the next day, 7 February, married Queen Wilhelmina in The Hague.
Their only child together, Princess Juliana, was born in 1909.
Henry also fathered at least one illegitimate child, Pim Lier by his mistress Willemina Martina Wenneker (1887–1973).
Born in 1918, Lier eventually rose to prominence in post-war Dutch politics as chairman of the extreme-right Centre Party.
The birth of a son out of wedlock was likely symptomatic of the duke's increasingly strained relationship with his wife.
Henry attended and even presided over the festivities, but Wilhelmina stayed away and stated that she was prevented from attending by her personal religious conviction that the type of event should not take place on a Sunday.
Henry became the 279th Knight Grand Cross of the Portuguese Order of the Tower and Sword, and in 1924, he was appointed as the 1,157th Knight of the Spanish Order of the Golden Fleece.
He died in The Hague, Netherlands, on 3 July 1934, aged 58.
Scouting

Henry successfully merged the two Dutch Boy Scout organisations Nederlandse Padvinders Organisatie (NPO, Netherlands Pathfinder Organisation) and the Nederlandse Padvinders Bond (NPB, Netherlands Pathfinder Federation) on 11 December 1915 to form De Nederlandse Padvinders (NPV, The Netherlands Pathfinders).
Extramarital relationships

Prince Henry was known to have had numerous extra-marital affairs.
It is rumored that he fathered between three and ten illegitimate children; however, firm proof remains elusive, except for Albrecht Willem Lier, known as the above-noted Pim Lier (22 July 1918 – 9 April 2015).
During her widowhood, Queen Wilhelmina paid monthly allowances to three known ex-mistresses: Julia Cervey in Geneva (ƒ200 per month), Wilhelmine Steiner in Zurich (ƒ500 per month), and Mien Lier-Wenneker (1887–1973), in The Hague (ƒ500 per month).
Mien Abbo-Wenneker (later Lier-Wenneker), gave birth to a total of six children; the older two, sisters Christina Margaretha Abbo and Edith Abbo (later Sheep-Abbo) were ostensibly the daughters of Mien's first husband, Dhr.
Abbo, but strongly rumored to have been fathered by Prince Henry.
In 1919, Mien married Lieutenant Jan Derk Lier, a former aide-de-camp to Prince Henry.
A grant of one hundred thousand guilders was arranged for Lt. Lier from the State by police chief François van 't Sant, whom Queen Wilhelmina engaged to verify the facts of her husband's extramarital relationships and children.
The male parent of the remaining three children was not verified as being either Prince Henry or Lt. Lier.
Subsequent to their birth, no additional allowance was settled on the family; in fact, the monthly allowance of one thousand guilders to Lt. Jan Derk Lier was halved by van't Sant after a short period, although the allowance to his wife continued.
Honours and awards

Ancestry

See also

References

External links

2 gave up the title "Prince of the Netherlands, but still held the title "Prince of Orange-Nassau"
3 title granted by Royal Decree to descendants of Princess Irene



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://www.w3.org/2003/11/swrl#> .
@prefix ns2: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

: a owl:Ontology ;
    dcterms:source <http://www.co-ode.org/roberts/family-tree.owl> .

:alsoKnownAs a owl:AnnotationProperty .

:formerlyKnownAs a owl:AnnotationProperty .

:hasBirthYear a rdfs:Datatype,
        owl:AnnotationProperty .

:hasDeathYear a owl:AnnotationProperty .

:hasMarriageYear a owl:AnnotationProperty .

:isAuntOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isSisterOf :isParentOf ) .

:isUncleOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    owl:propertyChainAxiom ( :isBrotherOf :isParentOf ) .

:knownAs a owl:AnnotationProperty .

dcterms:source a owl:AnnotationProperty .

ns2:isRuleEnabled a owl:AnnotationProperty .

:hasBrother a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isBrotherOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasDaughter a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isDaughterOf .

:hasFather a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Man ;
    rdfs:subPropertyOf :hasParent ;
    owl:inverseOf :isFatherOf .

:hasMother a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Woman ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf ;
    owl:inverseOf :isMotherOf .

:hasSister a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Woman ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:inverseOf :isSisterOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:hasSon a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Man ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf ;
    owl:inverseOf :isSonOf .

:isBloodrelationOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty .

:isDaughterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:isFatherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isMotherOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor,
        :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasChild,
        :isParentOf .

:isSonOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasParent,
        :isChildOf .

:DomainEntity a owl:Class .

:Female a owl:Class ;
    rdfs:subClassOf :Sex ;
    owl:disjointWith :Male .

:hasAncestor a owl:ObjectProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasRelation,
        owl:topObjectProperty ;
    owl:inverseOf :isAncestorOf .

:isBrotherOf a owl:ObjectProperty ;
    rdfs:domain :Man ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf ;
    owl:propertyDisjointWith :isChildOf,
        :isParentOf .

:Male a owl:Class ;
    rdfs:subClassOf :Sex .

:hasRelation a owl:ObjectProperty,
        owl:SymmetricProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person .

:hasSex a owl:FunctionalProperty,
        owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Sex .

:isAncestorOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :hasRelation .

:isSisterOf a owl:ObjectProperty ;
    rdfs:domain :Woman ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isSiblingOf .

:hasChild a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:inverseOf :isChildOf .

:hasParent a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor,
        :Person ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:equivalentProperty :isChildOf ;
    owl:inverseOf :isParentOf .

:isSiblingOf a owl:ObjectProperty,
        owl:SymmetricProperty,
        owl:TransitiveProperty ;
    rdfs:domain :Person ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isBloodrelationOf ;
    owl:propertyChainAxiom ( :hasParent :isParentOf ) .

:Sex a owl:Class ;
    rdfs:subClassOf :DomainEntity ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Female :Male ) ] .

:isChildOf a owl:ObjectProperty ;
    rdfs:domain :Person ;
    rdfs:range :Ancestor ;
    rdfs:subPropertyOf :hasAncestor ;
    owl:propertyDisjointWith :isSisterOf .

:x a ns1:Variable .

:Man a owl:Class ;
    owl:disjointWith :Sex,
        :Woman ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Male ] ) ] .

:isParentOf a owl:ObjectProperty ;
    rdfs:domain :Ancestor ;
    rdfs:range :Person ;
    rdfs:subPropertyOf :isAncestorOf ;
    owl:propertyDisjointWith :isSisterOf .

:Woman a owl:Class ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :hasSex ;
                        owl:someValuesFrom :Female ] ) ] .

:y a ns1:Variable .

:Ancestor a owl:Class ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:intersectionOf ( :Person [ a owl:Restriction ;
                        owl:onProperty :isAncestorOf ;
                        owl:someValuesFrom :Person ] ) ] .

:Person a owl:Class ;
    rdfs:subClassOf [ a owl:Restriction ;
            owl:onProperty :hasFather ;
            owl:someValuesFrom :Man ],
        [ a owl:Restriction ;
            owl:onProperty :hasMother ;
            owl:someValuesFrom :Woman ],
        [ a owl:Restriction ;
            owl:onProperty :hasSex ;
            owl:someValuesFrom :Sex ],
        [ a owl:Restriction ;
            owl:maxQualifiedCardinality "2"^^xsd:nonNegativeInteger ;
            owl:onClass :Person ;
            owl:onProperty :hasParent ],
        :DomainEntity ;
    owl:disjointWith :Sex ;
    owl:equivalentClass [ a owl:Class ;
            owl:unionOf ( :Man :Woman ) ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSon" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasBrother" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns1:Imp ;
    rdfs:label "infer hasSister" ;
    ns2:isRuleEnabled true ;
    rdfs:comment "" ;
    ns1:body [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns1:AtomList ;
                    rdf:first [ a ns1:ClassAtom ;
                            ns1:argument1 :y ;
                            ns1:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns1:head [ a ns1:AtomList ;
            rdf:first [ a ns1:IndividualPropertyAtom ;
                    ns1:argument1 :x ;
                    ns1:argument2 :y ;
                    ns1:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (b6af7324-f802-4795-9d8c-1c082e679a30)
 Call ID: b6af7324-f802-4795-9d8c-1c082e679a30
  Args:
    type: :Man
    source: :Henry_of_Mecklenburg-Schwerin
  AssignClass (e9c59268-f677-4bb5-8d5a-439b566cf1d4)
 Call ID: e9c59268-f677-4bb5-8d5a-439b566cf1d4
  Args:
    source: :Henry_of_Mecklenburg-Schwerin
    type: :Person
  AssignClass (1014f31d-14d5-4cd2-8558-9ba142ae1063)
 Call ID: 1014f31d-14d5-4cd2-8558-9ba142ae1063
  Args:
    type: :Ancestor
    source: :Henry_of_Mecklenburg-Schwerin
  AddLiteral (92653c01-b803-45d9-83a0-8b1b6b632b94)
 Call ID: 92653c01-b803-45d9-83a0-8b1b6b632b94
  Args:
    relation: :hasBirthYear
    literal_value: 1876
    source: :Henry_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AddLiteral (273ea2bc-f7a3-4f8e-bc0a-5a2c0cdd3f14)
 Call ID: 273ea2bc-f7a3-4f8e-bc0a-5a2c0cdd3f14
  Args:
    literal_type: xsd:integer
    source: :Henry_of_Mecklenburg-Schwerin
    literal_value: 1934
    relation: :hasDeathYear
  AssignClass (f10c97e3-3d77-40a1-8f2b-217442e54380)
 Call ID: f10c97e3-3d77-40a1-8f2b-217442e54380
  Args:
    source: :Frederick_Francis_II
    type: :Man
  AssignClass (1e703f11-9428-4603-9021-da9be1588ba1)
 Call ID: 1e703f11-9428-4603-9021-da9be1588ba1
  Args:
    type: :Person
    source: :Frederick_Francis_II
  AssignClass (a4fd7f9e-841b-4f6b-9ddc-14a851ba9d2e)
 Call ID: a4fd7f9e-841b-4f6b-9ddc-14a851ba9d2e
  Args:
    source: :Frederick_Francis_II
    type: :Ancestor
  AssignClass (24d0721d-3730-4f2e-9eb2-6eb6c0937888)
 Call ID: 24d0721d-3730-4f2e-9eb2-6eb6c0937888
  Args:
    type: :Woman
    source: :Marie_of_Schwarzburg-Rudolstadt
  AssignClass (eba7d65b-4063-4bb7-9a3c-05bb03e5a9d5)
 Call ID: eba7d65b-4063-4bb7-9a3c-05bb03e5a9d5
  Args:
    source: :Marie_of_Schwarzburg-Rudolstadt
    type: :Person
  AssignClass (bcb01b6a-2d49-44a2-ae38-2ef01bf72735)
 Call ID: bcb01b6a-2d49-44a2-ae38-2ef01bf72735
  Args:
    source: :Marie_of_Schwarzburg-Rudolstadt
    type: :Ancestor
  AddTriple (3422b253-ec7f-4476-82c2-b866bb1eeec3)
 Call ID: 3422b253-ec7f-4476-82c2-b866bb1eeec3
  Args:
    source: :Henry_of_Mecklenburg-Schwerin
    target: :Frederick_Francis_II
    relation: :hasFather
  AddTriple (78868dab-ced6-4d59-8fda-fbebf7b1fa23)
 Call ID: 78868dab-ced6-4d59-8fda-fbebf7b1fa23
  Args:
    relation: :hasMother
    target: :Marie_of_Schwarzburg-Rudolstadt
    source: :Henry_of_Mecklenburg-Schwerin
  AssignClass (8cd3f421-2f40-4830-b749-8a0ae8d47c52)
 Call ID: 8cd3f421-2f40-4830-b749-8a0ae8d47c52
  Args:
    source: :Queen_Wilhelmina
    type: :Woman
  AssignClass (a9e514f9-2a78-4d0d-93a9-cebe5c2878fa)
 Call ID: a9e514f9-2a78-4d0d-93a9-cebe5c2878fa
  Args:
    source: :Queen_Wilhelmina
    type: :Person
  AssignClass (582bb716-9a45-4234-9864-92eebf9be41c)
 Call ID: 582bb716-9a45-4234-9864-92eebf9be41c
  Args:
    source: :Queen_Wilhelmina
    type: :Ancestor
  AddTriple (a79b1400-47f4-4e02-bd89-b361c4c39995)
 Call ID: a79b1400-47f4-4e02-bd89-b361c4c39995
  Args:
    target: :Queen_Wilhelmina
    source: :Henry_of_Mecklenburg-Schwerin
    relation: :hasRelation
  AddLiteral (50139068-8998-4d81-adaf-8541ef88adab)
 Call ID: 50139068-8998-4d81-adaf-8541ef88adab
  Args:
    source: :Henry_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
    relation: :hasMarriageYear
    literal_value: 1901
  AssignClass (484074e5-c166-4941-a49d-60953fd32c02)
 Call ID: 484074e5-c166-4941-a49d-60953fd32c02
  Args:
    source: :Princess_Juliana
    type: :Woman
  AssignClass (00e5397b-a6f7-4448-90de-cfdf38443c60)
 Call ID: 00e5397b-a6f7-4448-90de-cfdf38443c60
  Args:
    type: :Person
    source: :Princess_Juliana
  AddTriple (d5f55ebd-c8a4-4070-907d-30e21fa32a7c)
 Call ID: d5f55ebd-c8a4-4070-907d-30e21fa32a7c
  Args:
    target: :Princess_Juliana
    source: :Henry_of_Mecklenburg-Schwerin
    relation: :hasChild
  AddTriple (f012af28-f8b9-4b6f-a45a-5dacd1caf94a)
 Call ID: f012af28-f8b9-4b6f-a45a-5dacd1caf94a
  Args:
    relation: :hasChild
    source: :Queen_Wilhelmina
    target: :Princess_Juliana
  AssignClass (7b2957aa-990d-43c3-95c6-0ace8605b50d)
 Call ID: 7b2957aa-990d-43c3-95c6-0ace8605b50d
  Args:
    source: :Pim_Lier
    type: :Man
  AssignClass (20993f77-cfac-48ae-a142-23bb12d725fb)
 Call ID: 20993f77-cfac-48ae-a142-23bb12d725fb
  Args:
    type: :Person
    source: :Pim_Lier
  AssignClass (f9a7eb96-8ab7-43fb-8d7b-66b6277ced30)
 Call ID: f9a7eb96-8ab7-43fb-8d7b-66b6277ced30
  Args:
    type: :Woman
    source: :Willemina_Martina_Wenneker
  AssignClass (f4ed1d6b-f0d1-4271-a5b6-d27b32389170)
 Call ID: f4ed1d6b-f0d1-4271-a5b6-d27b32389170
  Args:
    source: :Willemina_Martina_Wenneker
    type: :Person
  AddTriple (da4e21fc-6d4d-4d6a-913c-152c332ae395)
 Call ID: da4e21fc-6d4d-4d6a-913c-152c332ae395
  Args:
    relation: :hasChild
    source: :Henry_of_Mecklenburg-Schwerin
    target: :Pim_Lier
  AddTriple (5b28cf52-f10a-479d-9e60-af77f20d7fd1)
 Call ID: 5b28cf52-f10a-479d-9e60-af77f20d7fd1
  Args:
    relation: :hasChild
    source: :Willemina_Martina_Wenneker
    target: :Pim_Lier
  AssignClass (19e92f11-1aa3-4cf0-a74f-7a28b2a0b575)
 Call ID: 19e92f11-1aa3-4cf0-a74f-7a28b2a0b575
  Args:
    source: :Christina_Margaretha_Abbo
    type: :Woman
  AssignClass (c1451ad2-b4e6-4e44-9016-bffe8d0ec826)
 Call ID: c1451ad2-b4e6-4e44-9016-bffe8d0ec826
  Args:
    source: :Christina_Margaretha_Abbo
    type: :Person
  AssignClass (41c943ec-1b8e-40cf-8fbf-ff752a507fa0)
 Call ID: 41c943ec-1b8e-40cf-8fbf-ff752a507fa0
  Args:
    source: :Edith_Abbo
    type: :Woman
  AssignClass (3f90b648-204d-45a1-b068-82af2f2d4426)
 Call ID: 3f90b648-204d-45a1-b068-82af2f2d4426
  Args:
    source: :Edith_Abbo
    type: :Person
  AddTriple (03717d81-4a51-47d9-9af7-84d7be2a7cf0)
 Call ID: 03717d81-4a51-47d9-9af7-84d7be2a7cf0
  Args:
    target: :Christina_Margaretha_Abbo
    source: :Willemina_Martina_Wenneker
    relation: :hasChild
  AddTriple (ca514042-005e-471c-a815-ca4464d8973d)
 Call ID: ca514042-005e-471c-a815-ca4464d8973d
  Args:
    target: :Edith_Abbo
    source: :Willemina_Martina_Wenneker
    relation: :hasChild
  Finish (bbd72f63-0ff1-49c6-b2a3-dbcc83cbb274)
 Call ID: bbd72f63-0ff1-49c6-b2a3-dbcc83cbb274
  Args: