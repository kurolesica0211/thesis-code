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
  AssignClass (3bc1db33-9860-4b51-9b45-b2d6b213cb04)
 Call ID: 3bc1db33-9860-4b51-9b45-b2d6b213cb04
  Args:
    type: :Man
    source: :Henry_of_Mecklenburg-Schwerin
  AssignClass (34d885fc-400c-4f75-9cfd-d77c54e770b3)
 Call ID: 34d885fc-400c-4f75-9cfd-d77c54e770b3
  Args:
    type: :Person
    source: :Henry_of_Mecklenburg-Schwerin
  AddLiteral (dcb1152a-182c-47eb-95d2-d8183dc548df)
 Call ID: dcb1152a-182c-47eb-95d2-d8183dc548df
  Args:
    literal_type: xsd:integer
    source: :Henry_of_Mecklenburg-Schwerin
    literal_value: 1876
    relation: :hasBirthYear
  AddLiteral (2cca84c3-81b4-492d-9fee-196055c48e35)
 Call ID: 2cca84c3-81b4-492d-9fee-196055c48e35
  Args:
    relation: :hasDeathYear
    literal_value: 1934
    source: :Henry_of_Mecklenburg-Schwerin
    literal_type: xsd:integer
  AssignClass (472624b7-3b74-4f58-82d1-5e031146a59a)
 Call ID: 472624b7-3b74-4f58-82d1-5e031146a59a
  Args:
    type: :Man
    source: :Frederick_Francis_II
  AssignClass (ee7b53a9-eef9-4365-ba66-c1b77454ecd3)
 Call ID: ee7b53a9-eef9-4365-ba66-c1b77454ecd3
  Args:
    type: :Person
    source: :Frederick_Francis_II
  AssignClass (aa40646d-1827-45bf-a69d-f8addaf3d2a8)
 Call ID: aa40646d-1827-45bf-a69d-f8addaf3d2a8
  Args:
    type: :Woman
    source: :Marie_of_Schwarzburg-Rudolstadt
  AssignClass (4e958101-6e93-40b2-a921-3df0d3cff307)
 Call ID: 4e958101-6e93-40b2-a921-3df0d3cff307
  Args:
    type: :Person
    source: :Marie_of_Schwarzburg-Rudolstadt
  AddTriple (54f6418e-05f1-4a14-9a8c-9109d50cdf3e)
 Call ID: 54f6418e-05f1-4a14-9a8c-9109d50cdf3e
  Args:
    relation: :hasFather
    target: :Frederick_Francis_II
    source: :Henry_of_Mecklenburg-Schwerin
  AddTriple (a7c73309-17cc-460a-b24b-a4a52ff10f98)
 Call ID: a7c73309-17cc-460a-b24b-a4a52ff10f98
  Args:
    target: :Marie_of_Schwarzburg-Rudolstadt
    source: :Henry_of_Mecklenburg-Schwerin
    relation: :hasMother
  AssignClass (332fbda0-a7b9-4b1f-9367-388eb5d78f24)
 Call ID: 332fbda0-a7b9-4b1f-9367-388eb5d78f24
  Args:
    type: :Woman
    source: :Queen_Wilhelmina
  AssignClass (f8713aba-2b4e-4749-ad74-82e41aaeb0d3)
 Call ID: f8713aba-2b4e-4749-ad74-82e41aaeb0d3
  Args:
    type: :Person
    source: :Queen_Wilhelmina
  AddLiteral (fdebc088-4824-4bb7-acc6-51b8bdb0f575)
 Call ID: fdebc088-4824-4bb7-acc6-51b8bdb0f575
  Args:
    literal_type: xsd:integer
    source: :Henry_of_Mecklenburg-Schwerin
    relation: :hasMarriageYear
    literal_value: 1901
  AddTriple (a5c4a237-c942-4343-a71c-a9cb3be2fe9d)
 Call ID: a5c4a237-c942-4343-a71c-a9cb3be2fe9d
  Args:
    relation: :hasRelation
    target: :Queen_Wilhelmina
    source: :Henry_of_Mecklenburg-Schwerin
  AssignClass (e7ba7c7b-dfd8-46a6-9516-b9bb0b4b277d)
 Call ID: e7ba7c7b-dfd8-46a6-9516-b9bb0b4b277d
  Args:
    type: :Woman
    source: :Princess_Juliana
  AssignClass (ca012469-f513-4943-be27-f29432b1103e)
 Call ID: ca012469-f513-4943-be27-f29432b1103e
  Args:
    type: :Person
    source: :Princess_Juliana
  AddTriple (468545c8-5ceb-4c3f-8e75-2db9a43016dd)
 Call ID: 468545c8-5ceb-4c3f-8e75-2db9a43016dd
  Args:
    source: :Princess_Juliana
    target: :Henry_of_Mecklenburg-Schwerin
    relation: :isChildOf
  AddTriple (c33b3b83-bdad-46de-9094-3567bb5a2dbf)
 Call ID: c33b3b83-bdad-46de-9094-3567bb5a2dbf
  Args:
    relation: :isChildOf
    target: :Queen_Wilhelmina
    source: :Princess_Juliana
  AssignClass (1350a3bd-0be3-4f57-9dc7-022202acdbfa)
 Call ID: 1350a3bd-0be3-4f57-9dc7-022202acdbfa
  Args:
    type: :Man
    source: :Pim_Lier
  AssignClass (d9a89d57-aa38-42ed-b7c4-1edc96200b4b)
 Call ID: d9a89d57-aa38-42ed-b7c4-1edc96200b4b
  Args:
    type: :Person
    source: :Pim_Lier
  AssignClass (7bb05bfb-29b8-4293-acab-3c69d0d8f04b)
 Call ID: 7bb05bfb-29b8-4293-acab-3c69d0d8f04b
  Args:
    type: :Woman
    source: :Willemina_Martina_Wenneker
  AssignClass (c517c00a-dcb6-4652-86f8-2c5721d38c14)
 Call ID: c517c00a-dcb6-4652-86f8-2c5721d38c14
  Args:
    type: :Person
    source: :Willemina_Martina_Wenneker
  AddTriple (3519dd79-7e7c-420c-b13c-f5861a02aebc)
 Call ID: 3519dd79-7e7c-420c-b13c-f5861a02aebc
  Args:
    relation: :isChildOf
    target: :Henry_of_Mecklenburg-Schwerin
    source: :Pim_Lier
  AddTriple (c3d85888-ef66-4d3a-ab87-aa68a6f42c0b)
 Call ID: c3d85888-ef66-4d3a-ab87-aa68a6f42c0b
  Args:
    target: :Willemina_Martina_Wenneker
    source: :Pim_Lier
    relation: :isChildOf
  AssignClass (664d2a66-f4f1-49d0-be39-f64a3de744bc)
 Call ID: 664d2a66-f4f1-49d0-be39-f64a3de744bc
  Args:
    type: :Woman
    source: :Christina_Margaretha_Abbo
  AssignClass (fad2de31-43dd-4ab7-8510-9cf57edd51c8)
 Call ID: fad2de31-43dd-4ab7-8510-9cf57edd51c8
  Args:
    type: :Person
    source: :Christina_Margaretha_Abbo
  AssignClass (b32c8333-8133-484c-8137-694e6478b55c)
 Call ID: b32c8333-8133-484c-8137-694e6478b55c
  Args:
    type: :Woman
    source: :Edith_Abbo
  AssignClass (e06e1bd2-2708-4d74-8936-2a872a996d92)
 Call ID: e06e1bd2-2708-4d74-8936-2a872a996d92
  Args:
    type: :Person
    source: :Edith_Abbo
  AddTriple (aa574f3a-b9cf-44e4-b20f-768138810bec)
 Call ID: aa574f3a-b9cf-44e4-b20f-768138810bec
  Args:
    source: :Christina_Margaretha_Abbo
    target: :Willemina_Martina_Wenneker
    relation: :isChildOf
  AddTriple (84718c06-de3f-4023-b0db-83613b34bf66)
 Call ID: 84718c06-de3f-4023-b0db-83613b34bf66
  Args:
    relation: :isChildOf
    source: :Edith_Abbo
    target: :Willemina_Martina_Wenneker
  Finish (871b5f3a-c956-4260-b44f-f972e7cb84f5)
 Call ID: 871b5f3a-c956-4260-b44f-f972e7cb84f5
  Args: