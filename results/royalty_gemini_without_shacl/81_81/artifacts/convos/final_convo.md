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
Prince Vincent of Denmark, Count of Monpezat RE (Vincent Frederik Minik Alexander; born 8 January 2011) is a member of the Danish royal family.
He is the third child and younger son of King Frederik X and Queen Mary, the sixth grandchild and youngest grandson of Queen Margrethe II and Prince Henrik, and the older twin brother of Princess Josephine.
Vincent is third in line to the Danish throne, after his older brother, Crown Prince Christian, and older sister, Princess Isabella.
Birth and early life

Queen Margrethe II


Vincent was born on 8 January 2011 at Rigshospitalet, the Copenhagen University Hospital, in Copenhagen, at 10:30 am local time, 26 minutes before his twin sister.
Shortly after the birth, while speaking to the press, the Crown Prince joked about calling his newborn son Elvis, as the twins share a birthday with Elvis Presley.
Vincent and his sister were baptised by the royal confessor, the Bishop of Copenhagen Erik Norman Svendsen, on 14 April at the Church of Holmen in central Copenhagen.
The twins were baptised at the royal baptismal font which has been used for the baptism of royal children in Denmark since 1671.
Prince Vincent wore the royal christening gown which was made for his great-great-grandfather, King Christian X, in 1870, while his sister wore a gown found among Queen Ingrid's belongings.
His name was announced as Vincent Frederik Minik Alexander.
His godparents are his maternal uncle, John Stuart Donaldson; his father's first cousin, the Prince of Sayn-Wittgenstein-Berleburg (then the Hereditary Prince); his mother's lady-in-waiting, Caroline Heering; and friends of his parents, the King of Spain (then the Prince of Asturias), Count Michael Ahlefeldt-Laurvig-Bille and Baroness Helle Reedtz-Thott.
Under the old system of male-preference primogeniture, Vincent would have displaced his elder sister Isabella in the line of succession; with the new law, he comes directly after her instead.
On 15 August 2017, Vincent and his younger twin sister started school at Tranegårdsskolen in Gentofte – the same public school as their elder siblings.
Titles, styles, and honours

Vincent is styled as His Royal Highness Prince Vincent of Denmark, Count of Monpezat.



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
  AssignClass (a8bd0bb7-ba7f-4493-ad6f-a658f183efde)
 Call ID: a8bd0bb7-ba7f-4493-ad6f-a658f183efde
  Args:
    type: :Man
    source: :PrinceVincentOfDenmark
  AssignClass (1af2c543-0461-4393-ab61-a65f71e792bd)
 Call ID: 1af2c543-0461-4393-ab61-a65f71e792bd
  Args:
    source: :PrinceVincentOfDenmark
    type: :Person
  AddLiteral (279cfb60-781a-46b0-abef-ff2c66968304)
 Call ID: 279cfb60-781a-46b0-abef-ff2c66968304
  Args:
    relation: :hasBirthYear
    source: :PrinceVincentOfDenmark
    literal_value: 2011
    literal_type: xsd:integer
  AssignClass (8319ca4d-070e-4739-84ba-b0a06db395d4)
 Call ID: 8319ca4d-070e-4739-84ba-b0a06db395d4
  Args:
    source: :KingFrederikX
    type: :Man
  AssignClass (63149694-08ce-4f92-9202-59401fc8995d)
 Call ID: 63149694-08ce-4f92-9202-59401fc8995d
  Args:
    source: :KingFrederikX
    type: :Person
  AssignClass (ec1e07aa-de82-4244-bf2c-0ad4febfd2c8)
 Call ID: ec1e07aa-de82-4244-bf2c-0ad4febfd2c8
  Args:
    type: :Woman
    source: :QueenMary
  AssignClass (c2c0446a-a653-4461-a118-cb642d7bdbd4)
 Call ID: c2c0446a-a653-4461-a118-cb642d7bdbd4
  Args:
    source: :QueenMary
    type: :Person
  AddTriple (75aa68f1-79c2-4369-b24d-427d118204e7)
 Call ID: 75aa68f1-79c2-4369-b24d-427d118204e7
  Args:
    relation: :hasFather
    target: :KingFrederikX
    source: :PrinceVincentOfDenmark
  AddTriple (6f3c0639-4f6e-4bda-aa84-4f03e7e742ad)
 Call ID: 6f3c0639-4f6e-4bda-aa84-4f03e7e742ad
  Args:
    source: :PrinceVincentOfDenmark
    target: :QueenMary
    relation: :hasMother
  AssignClass (ba4e630e-4546-4156-8d57-9496ef147c63)
 Call ID: ba4e630e-4546-4156-8d57-9496ef147c63
  Args:
    type: :Woman
    source: :QueenMargretheII
  AssignClass (299a2de7-3856-41e4-8d89-95359d1fb25f)
 Call ID: 299a2de7-3856-41e4-8d89-95359d1fb25f
  Args:
    source: :QueenMargretheII
    type: :Person
  AssignClass (3dcc1e62-09e3-40e1-b1ad-fb2e1d839dc1)
 Call ID: 3dcc1e62-09e3-40e1-b1ad-fb2e1d839dc1
  Args:
    type: :Man
    source: :PrinceHenrik
  AssignClass (8af12736-9368-48b9-8e08-183679ef9d65)
 Call ID: 8af12736-9368-48b9-8e08-183679ef9d65
  Args:
    type: :Person
    source: :PrinceHenrik
  AddTriple (93a59e66-899f-42f8-abb4-c16dfc084589)
 Call ID: 93a59e66-899f-42f8-abb4-c16dfc084589
  Args:
    source: :KingFrederikX
    target: :QueenMargretheII
    relation: :hasParent
  AddTriple (c5644544-a75d-4995-af3b-10ab66c4efc2)
 Call ID: c5644544-a75d-4995-af3b-10ab66c4efc2
  Args:
    relation: :hasParent
    target: :PrinceHenrik
    source: :KingFrederikX
  AssignClass (463411a8-e20b-4c31-852e-3d0ecf1239fe)
 Call ID: 463411a8-e20b-4c31-852e-3d0ecf1239fe
  Args:
    source: :PrincessJosephine
    type: :Woman
  AssignClass (72a2d3c1-8dff-4b66-bcd8-8f374d6870c7)
 Call ID: 72a2d3c1-8dff-4b66-bcd8-8f374d6870c7
  Args:
    type: :Person
    source: :PrincessJosephine
  AddTriple (4e30478f-669e-4bd8-be66-7ac57fed9ef0)
 Call ID: 4e30478f-669e-4bd8-be66-7ac57fed9ef0
  Args:
    relation: :isSiblingOf
    target: :PrincessJosephine
    source: :PrinceVincentOfDenmark
  AssignClass (cef9f108-1dd4-43f7-a35e-851595ddf02a)
 Call ID: cef9f108-1dd4-43f7-a35e-851595ddf02a
  Args:
    type: :Man
    source: :CrownPrinceChristian
  AssignClass (0e54132d-49aa-4948-bea0-f34f730fa012)
 Call ID: 0e54132d-49aa-4948-bea0-f34f730fa012
  Args:
    source: :CrownPrinceChristian
    type: :Person
  AddTriple (21364cf2-e576-4a57-957f-204a1d04acb8)
 Call ID: 21364cf2-e576-4a57-957f-204a1d04acb8
  Args:
    target: :CrownPrinceChristian
    source: :PrinceVincentOfDenmark
    relation: :isSiblingOf
  AssignClass (dbf5695e-00b7-4818-b1c4-9a5ffa49c41a)
 Call ID: dbf5695e-00b7-4818-b1c4-9a5ffa49c41a
  Args:
    source: :PrincessIsabella
    type: :Woman
  AssignClass (9b0690a4-8be6-48b9-af59-1622880c7758)
 Call ID: 9b0690a4-8be6-48b9-af59-1622880c7758
  Args:
    type: :Person
    source: :PrincessIsabella
  AddTriple (89d9262b-8b5b-4217-9716-9e5516427e85)
 Call ID: 89d9262b-8b5b-4217-9716-9e5516427e85
  Args:
    target: :PrincessIsabella
    source: :PrinceVincentOfDenmark
    relation: :isSiblingOf
  AssignClass (fcb4299c-163b-4f65-ac17-50d79c40fdef)
 Call ID: fcb4299c-163b-4f65-ac17-50d79c40fdef
  Args:
    type: :Man
    source: :KingChristianX
  AssignClass (53ec46fb-7a9d-4a5c-950c-09ef4789bb24)
 Call ID: 53ec46fb-7a9d-4a5c-950c-09ef4789bb24
  Args:
    source: :KingChristianX
    type: :Person
  AddTriple (32b30229-fa08-4264-a65a-97e8992b8054)
 Call ID: 32b30229-fa08-4264-a65a-97e8992b8054
  Args:
    relation: :hasAncestor
    source: :PrinceVincentOfDenmark
    target: :KingChristianX
  AssignClass (84ba91cc-16f5-44f1-a5aa-ba4ad1400cc4)
 Call ID: 84ba91cc-16f5-44f1-a5aa-ba4ad1400cc4
  Args:
    source: :QueenIngrid
    type: :Woman
  AssignClass (fb0bb00f-a3e0-494c-8a2b-33d68812fda4)
 Call ID: fb0bb00f-a3e0-494c-8a2b-33d68812fda4
  Args:
    source: :QueenIngrid
    type: :Person
  Finish (96ea1b1b-77f8-4f32-b73e-6b41bf091e19)
 Call ID: 96ea1b1b-77f8-4f32-b73e-6b41bf091e19
  Args: