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
Princess Nathalie of Sayn-Wittgenstein-Berleburg (Nathalie Xenia Margrethe Benedikte; born 2 May 1975) is a Danish equestrian, an Olympian, and the daughter of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She is the niece of Queen Margrethe II of Denmark and King Constantine II of Greece.
Her first cousin is King Frederik X of Denmark.
Early life

Princess Nathalie was born on 2 May 1975 in Copenhagen, Denmark, the youngest of three children of Princess Benedikte of Denmark and Prince Richard of Sayn-Wittgenstein-Berleburg.
She grew up at Schloss Berleburg in Bad Berleburg, Germany.
Nathalie and her sister Alexandra became Danish citizens on 19 May 1998.
Neither she nor her siblings are in line of succession to the Danish throne, as that would have required taking up permanent residence in Denmark when reaching the age of mandatory education.
Equestrian career

In 1994, Princess Nathalie began training at the Swedish stud Flyinge with Kyra Kyrklund, a former world champion in dressage.
Nathalie was selected as a reserve rider for the 2000 Olympic team.
She finished 12th in the individual event and helped Denmark to a 4th-place team finish.
In January 2017, Nathalie was named head coach of the Danish national dressage team.
In autumn 2005, she opened her own stud farm, which is based in Bad Berleburg.
Marriage and children

On 4 January 2010, Princess Nathalie's engagement to German horse breeder Alexander Johannsmann (born 6 December 1977), son of showjumper Heinrich-Wilhelm Johannsmann, was announced.
The couple married civilly 27 May 2010 and religiously the following year, on 18 June 2011 at the Protestant Stadtkirche in Berleburg, Germany.
Princess Nathalie gave birth to a son, Konstantin Gustav Heinrich Richard, on 24 July 2010.
Konstantin's godparents were Crown Princess Mary of Denmark, his aunt Ann-Kathrin Johannsmann, and his uncle Prince Gustav.
On 28 January 2015, she gave birth to her second child, a daughter named Louisa Margareta Benedikte Hanna, in Bad Berleburg, Germany.
On 15 August 2022, the Danish court confirmed that Nathalie and Johannsmann had divorced.



### Ontology Definition:
@prefix : <http://example.com/family_TBOX.ttl#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix ns1: <http://swrl.stanford.edu/ontologies/3.3/swrla.owl#> .
@prefix ns2: <http://www.w3.org/2003/11/swrl#> .
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

ns1:isRuleEnabled a owl:AnnotationProperty .

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

:x a ns2:Variable .

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

:y a ns2:Variable .

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

[] a ns2:Imp ;
    rdfs:label "infer hasSon" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSon ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasBrother" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Man ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasBrother ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasDaughter" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasChild ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasDaughter ] ;
            rdf:rest () ] .

[] a ns2:Imp ;
    rdfs:label "infer hasSister" ;
    ns1:isRuleEnabled true ;
    rdfs:comment "" ;
    ns2:body [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :isSiblingOf ] ;
            rdf:rest [ a ns2:AtomList ;
                    rdf:first [ a ns2:ClassAtom ;
                            ns2:argument1 :y ;
                            ns2:classPredicate :Woman ] ;
                    rdf:rest () ] ] ;
    ns2:head [ a ns2:AtomList ;
            rdf:first [ a ns2:IndividualPropertyAtom ;
                    ns2:argument1 :x ;
                    ns2:argument2 :y ;
                    ns2:propertyPredicate :hasSister ] ;
            rdf:rest () ] .



### Current Data Graph State:



---
**Requirement**: Process the text and use the available tools to make the Data Graph a **faithful and evidence-based** representation of the facts presented in the text. 

**Strict Instruction**: Do not add any information or entities (like extra marriages or family members) that are not specifically named or described in the Input Text, even if you know they exist historically. Start by analyzing the text and then proceed with tool calls.

================================== Ai Message ==================================

[]
Tool Calls:
  AssignClass (2eccf449-6ff4-4b68-9d8a-dd91c5c4b132)
 Call ID: 2eccf449-6ff4-4b68-9d8a-dd91c5c4b132
  Args:
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (c53091a1-5aa8-4a02-a922-e45b7068be0c)
 Call ID: c53091a1-5aa8-4a02-a922-e45b7068be0c
  Args:
    type: :Woman
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddLiteral (625a049e-8876-4d81-9dee-d207fc2a6afa)
 Call ID: 625a049e-8876-4d81-9dee-d207fc2a6afa
  Args:
    literal_value: 1975
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
  AssignClass (90da8adb-16d8-4ed4-bb20-d1c4a117c95d)
 Call ID: 90da8adb-16d8-4ed4-bb20-d1c4a117c95d
  Args:
    type: :Person
    source: Benedikte_of_Denmark
  AssignClass (0e22ad67-8e05-4469-b7db-f6d421c04189)
 Call ID: 0e22ad67-8e05-4469-b7db-f6d421c04189
  Args:
    type: :Woman
    source: Benedikte_of_Denmark
  AssignClass (4cf3ee12-a9f5-41a2-8840-e1754982fb6f)
 Call ID: 4cf3ee12-a9f5-41a2-8840-e1754982fb6f
  Args:
    source: Richard_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (366bd1c9-dbfc-4f69-bea3-e849f92d5c4f)
 Call ID: 366bd1c9-dbfc-4f69-bea3-e849f92d5c4f
  Args:
    type: :Man
    source: Richard_of_Sayn-Wittgenstein-Berleburg
  AddTriple (0569d017-21dc-49c9-ad41-a31120793125)
 Call ID: 0569d017-21dc-49c9-ad41-a31120793125
  Args:
    relation: :hasMother
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    target: Benedikte_of_Denmark
  AddTriple (488348b5-6346-417b-9259-9b1f678f0fc4)
 Call ID: 488348b5-6346-417b-9259-9b1f678f0fc4
  Args:
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :hasFather
    target: Richard_of_Sayn-Wittgenstein-Berleburg
  AssignClass (0fa8f0c2-d9ea-41a5-b71d-caf6707ebca0)
 Call ID: 0fa8f0c2-d9ea-41a5-b71d-caf6707ebca0
  Args:
    source: Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Person
  AssignClass (0c739104-258f-44ad-a639-3ffc76b000de)
 Call ID: 0c739104-258f-44ad-a639-3ffc76b000de
  Args:
    source: Alexandra_of_Sayn-Wittgenstein-Berleburg
    type: :Woman
  AddTriple (079f8bc8-603f-4919-afa5-eb94146ff2c4)
 Call ID: 079f8bc8-603f-4919-afa5-eb94146ff2c4
  Args:
    relation: :isSiblingOf
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    target: Alexandra_of_Sayn-Wittgenstein-Berleburg
  AssignClass (1bd683a8-d6bc-43b2-b388-bb3fbef2a893)
 Call ID: 1bd683a8-d6bc-43b2-b388-bb3fbef2a893
  Args:
    source: Alexander_Johannsmann
    type: :Person
  AssignClass (a9271cff-7a6a-4f8a-828e-6e308a90d454)
 Call ID: a9271cff-7a6a-4f8a-828e-6e308a90d454
  Args:
    source: Alexander_Johannsmann
    type: :Man
  AddLiteral (b944c605-7861-4858-a665-456ab1a0035e)
 Call ID: b944c605-7861-4858-a665-456ab1a0035e
  Args:
    literal_value: 1977
    relation: :hasBirthYear
    source: Alexander_Johannsmann
    literal_type: xsd:integer
  AddLiteral (301f1644-234d-4188-bd3f-5e4089fc7078)
 Call ID: 301f1644-234d-4188-bd3f-5e4089fc7078
  Args:
    literal_value: 2010
    source: Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMarriageYear
    literal_type: xsd:integer
  AssignClass (8990b595-f478-488d-b2ab-b6626778cefe)
 Call ID: 8990b595-f478-488d-b2ab-b6626778cefe
  Args:
    source: Heinrich-Wilhelm_Johannsmann
    type: :Person
  AssignClass (1de6f2c4-dab5-41a1-b329-db1e6f9243e6)
 Call ID: 1de6f2c4-dab5-41a1-b329-db1e6f9243e6
  Args:
    type: :Man
    source: Heinrich-Wilhelm_Johannsmann
  AddTriple (1904c1b9-4c60-4ced-b44b-633378282b83)
 Call ID: 1904c1b9-4c60-4ced-b44b-633378282b83
  Args:
    target: Heinrich-Wilhelm_Johannsmann
    relation: :hasFather
    source: Alexander_Johannsmann
  AssignClass (f1ef790a-9183-4c61-93c3-d47f4a648ca2)
 Call ID: f1ef790a-9183-4c61-93c3-d47f4a648ca2
  Args:
    type: :Person
    source: Konstantin_Gustav_Heinrich_Richard
  AssignClass (cb72be7e-20c5-4c06-87e1-1ad70ca4dbd0)
 Call ID: cb72be7e-20c5-4c06-87e1-1ad70ca4dbd0
  Args:
    type: :Man
    source: Konstantin_Gustav_Heinrich_Richard
  AddTriple (9456a050-cfeb-489f-b785-c133ae34b249)
 Call ID: 9456a050-cfeb-489f-b785-c133ae34b249
  Args:
    target: Nathalie_of_Sayn-Wittgenstein-Berleburg
    relation: :hasMother
    source: Konstantin_Gustav_Heinrich_Richard
  AddTriple (6dc0f241-0581-4701-97ac-9f88d01c4228)
 Call ID: 6dc0f241-0581-4701-97ac-9f88d01c4228
  Args:
    target: Alexander_Johannsmann
    relation: :hasFather
    source: Konstantin_Gustav_Heinrich_Richard
  AssignClass (c35f020a-567f-4348-b05d-2ddf4682b85b)
 Call ID: c35f020a-567f-4348-b05d-2ddf4682b85b
  Args:
    type: :Person
    source: Louisa_Margareta_Benedikte_Hanna
  AssignClass (748a085c-f3ac-4d5b-9ce1-c41ce1fe6568)
 Call ID: 748a085c-f3ac-4d5b-9ce1-c41ce1fe6568
  Args:
    source: Louisa_Margareta_Benedikte_Hanna
    type: :Woman
  AddTriple (4f4b6c5a-fbd4-41ed-8024-b54e44aa70c5)
 Call ID: 4f4b6c5a-fbd4-41ed-8024-b54e44aa70c5
  Args:
    relation: :hasMother
    source: Louisa_Margareta_Benedikte_Hanna
    target: Nathalie_of_Sayn-Wittgenstein-Berleburg
  AddTriple (03031ecf-c92c-4694-9338-3d8d75af5898)
 Call ID: 03031ecf-c92c-4694-9338-3d8d75af5898
  Args:
    target: Alexander_Johannsmann
    source: Louisa_Margareta_Benedikte_Hanna
    relation: :hasFather
  AssignClass (8470cf45-e06e-4220-8e30-68c38252f215)
 Call ID: 8470cf45-e06e-4220-8e30-68c38252f215
  Args:
    source: Ann-Kathrin_Johannsmann
    type: :Person
  AssignClass (4334ecd6-6356-4ba0-91cf-515f91879c65)
 Call ID: 4334ecd6-6356-4ba0-91cf-515f91879c65
  Args:
    source: Ann-Kathrin_Johannsmann
    type: :Woman
  AssignClass (6bb424ed-9abe-4790-a75c-1055c3d520aa)
 Call ID: 6bb424ed-9abe-4790-a75c-1055c3d520aa
  Args:
    type: :Person
    source: Gustav_of_Sayn-Wittgenstein-Berleburg
  AssignClass (516ac1b5-264a-4f13-b5cc-e7eb50a078a0)
 Call ID: 516ac1b5-264a-4f13-b5cc-e7eb50a078a0
  Args:
    source: Gustav_of_Sayn-Wittgenstein-Berleburg
    type: :Man
  Finish (046a5181-b3f7-46c1-ae54-baf2b3c45088)
 Call ID: 046a5181-b3f7-46c1-ae54-baf2b3c45088
  Args: