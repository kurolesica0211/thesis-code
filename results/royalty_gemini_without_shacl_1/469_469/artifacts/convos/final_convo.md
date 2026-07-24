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
Countess Walburga Douglas (née von Habsburg-Lothringen; born 5 October 1958) is a German-born Swedish lawyer and politician, who served as a member of the Riksdag of Sweden for the Moderate Party from 2006 to 2014.
Early life

Born in 1958 in Berg am Starnberger See, West Germany, she is the fifth daughter of Otto von Habsburg, the last crown prince of Austria-Hungary, and his wife Princess Regina of Saxe-Meiningen.
Walburga was banished from the Republic of Austria from birth and well into adult life, along with her siblings, by the Habsburg Law that had been in effect since 1938, having been (re)imposed by the Nazis.
She is a granddaughter of the last Austrian emperor, Charles I, and a member of the House of Habsburg-Lorraine.
Her ancestral titles (abolished in Austria since 1919) are Archduchess Walburga of Austria, Archduchess of Austria, Princess of Hungary and Bohemia, with the style of Her Imperial and Royal Highness (HI&RH).
She does not currently use her ancestral titles actively in her daily life; however, by law she holds the title of Countess Douglas in the Kingdom of Sweden, her current country of residence and citizenship.
On 17 September 2023, Douglas visited Armenia to dedicate the opening of the PanEuropa Armenia branch in Yerevan.
Personal life

On 5 December 1992 in Budapest, Hungary, Walburga married a Swedish nobleman, Count Carl Axel Archibald Douglas (born 27 November 1949 in Stockholm), son of Count Archibald Douglas and Baroness Margareta Lagerfelt.
Her husband's family is a  noble family in Sweden, descended from the Scot Robert Douglas, Count of Skenninge, member of the Scottish Clan Douglas and founder of its Swedish branch.
Her husband is a first cousin of Count Gustaf Douglas and his sisters Rosita Spencer-Churchill, Duchess of Marlborough, and Princess Elisabeth, Duchess in Bavaria, the wife of Prince Max, Duke in Bavaria.
They have a son, Count Mauritz Otto Wenzel Douglas (born 30 March 1994 in Stockholm).



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
  AssignClass (74d5db84-5640-4230-a834-798509e76527)
 Call ID: 74d5db84-5640-4230-a834-798509e76527
  Args:
    source: :WalburgaDouglas
    type: :Woman
  AssignClass (934e0cdd-8e68-4ca9-b8c1-cfd92ee31952)
 Call ID: 934e0cdd-8e68-4ca9-b8c1-cfd92ee31952
  Args:
    source: :WalburgaDouglas
    type: :Person
  AddLiteral (a6f146d4-c966-4207-a94a-f42febb5cf0c)
 Call ID: a6f146d4-c966-4207-a94a-f42febb5cf0c
  Args:
    literal_type: xsd:integer
    literal_value: 1958
    source: :WalburgaDouglas
    relation: :hasBirthYear
  AssignClass (a9bb5bc0-f306-4900-99d2-f6537b3c7d84)
 Call ID: a9bb5bc0-f306-4900-99d2-f6537b3c7d84
  Args:
    type: :Man
    source: :OttoVonHabsburg
  AssignClass (8420bb12-947a-490b-b1c6-bab2a1569ef0)
 Call ID: 8420bb12-947a-490b-b1c6-bab2a1569ef0
  Args:
    source: :OttoVonHabsburg
    type: :Person
  AssignClass (d9864044-4569-4af2-931c-280ea8ecdd32)
 Call ID: d9864044-4569-4af2-931c-280ea8ecdd32
  Args:
    source: :OttoVonHabsburg
    type: :Ancestor
  AssignClass (89824625-f0d7-4067-84b2-4faf13915943)
 Call ID: 89824625-f0d7-4067-84b2-4faf13915943
  Args:
    source: :ReginaOfSaxeMeiningen
    type: :Woman
  AssignClass (cf52272c-2b21-441f-b662-25fd8140c6ff)
 Call ID: cf52272c-2b21-441f-b662-25fd8140c6ff
  Args:
    source: :ReginaOfSaxeMeiningen
    type: :Person
  AssignClass (9bec28fe-dd62-4733-9d84-bab453248213)
 Call ID: 9bec28fe-dd62-4733-9d84-bab453248213
  Args:
    type: :Ancestor
    source: :ReginaOfSaxeMeiningen
  AddTriple (4de9dda1-55aa-4811-bbaa-2f673ac34ddf)
 Call ID: 4de9dda1-55aa-4811-bbaa-2f673ac34ddf
  Args:
    source: :WalburgaDouglas
    target: :OttoVonHabsburg
    relation: :isDaughterOf
  AddTriple (21e6a6a9-06ee-4d83-aa45-96014e97d216)
 Call ID: 21e6a6a9-06ee-4d83-aa45-96014e97d216
  Args:
    relation: :isDaughterOf
    target: :ReginaOfSaxeMeiningen
    source: :WalburgaDouglas
  AssignClass (03678987-5c25-4993-8919-fdcaa91eeb9e)
 Call ID: 03678987-5c25-4993-8919-fdcaa91eeb9e
  Args:
    type: :Man
    source: :CarlAxelArchibaldDouglas
  AssignClass (2a3e7806-8a8e-464d-91fe-0b391be80393)
 Call ID: 2a3e7806-8a8e-464d-91fe-0b391be80393
  Args:
    source: :CarlAxelArchibaldDouglas
    type: :Person
  AddLiteral (46397b72-fa5a-441c-b1cd-e528e9c320da)
 Call ID: 46397b72-fa5a-441c-b1cd-e528e9c320da
  Args:
    relation: :hasBirthYear
    literal_type: xsd:integer
    source: :CarlAxelArchibaldDouglas
    literal_value: 1949
  AddTriple (e5542a39-a416-4fb2-874e-2eb9f955cdb2)
 Call ID: e5542a39-a416-4fb2-874e-2eb9f955cdb2
  Args:
    target: :CarlAxelArchibaldDouglas
    relation: :hasRelation
    source: :WalburgaDouglas
  AddLiteral (42227318-7e34-492b-8325-5d5ba1e433c2)
 Call ID: 42227318-7e34-492b-8325-5d5ba1e433c2
  Args:
    relation: :hasMarriageYear
    source: :WalburgaDouglas
    literal_value: 1992
    literal_type: xsd:integer
  AssignClass (8c7074c3-314d-4c57-9f2b-3e27cd20d9ab)
 Call ID: 8c7074c3-314d-4c57-9f2b-3e27cd20d9ab
  Args:
    source: :ArchibaldDouglas
    type: :Man
  AssignClass (e4593d33-13d5-4aa9-99cc-b1b6c74b6147)
 Call ID: e4593d33-13d5-4aa9-99cc-b1b6c74b6147
  Args:
    type: :Person
    source: :ArchibaldDouglas
  AssignClass (b2ca4e9a-192a-4a89-b3be-c048c4b0389f)
 Call ID: b2ca4e9a-192a-4a89-b3be-c048c4b0389f
  Args:
    type: :Woman
    source: :MargaretaLagerfelt
  AssignClass (8a16c9be-7a9f-4e41-ba45-0670a22872fc)
 Call ID: 8a16c9be-7a9f-4e41-ba45-0670a22872fc
  Args:
    source: :MargaretaLagerfelt
    type: :Person
  AddTriple (7e7dc5a7-f52d-4f5e-b578-e91d39ebee22)
 Call ID: 7e7dc5a7-f52d-4f5e-b578-e91d39ebee22
  Args:
    source: :CarlAxelArchibaldDouglas
    relation: :isSonOf
    target: :ArchibaldDouglas
  AddTriple (09f4b917-b667-41e7-a04e-6efac95f9612)
 Call ID: 09f4b917-b667-41e7-a04e-6efac95f9612
  Args:
    source: :CarlAxelArchibaldDouglas
    relation: :isSonOf
    target: :MargaretaLagerfelt
  AssignClass (b055cb0d-f196-4cd7-a347-159015f3e61b)
 Call ID: b055cb0d-f196-4cd7-a347-159015f3e61b
  Args:
    source: :MauritzOttoWenzelDouglas
    type: :Man
  AssignClass (2ec4cf77-1599-4166-a4b7-6b82d66799c6)
 Call ID: 2ec4cf77-1599-4166-a4b7-6b82d66799c6
  Args:
    type: :Person
    source: :MauritzOttoWenzelDouglas
  AddLiteral (409a25b5-8ecd-41fd-9bbe-9d619104ffcd)
 Call ID: 409a25b5-8ecd-41fd-9bbe-9d619104ffcd
  Args:
    literal_value: 1994
    source: :MauritzOttoWenzelDouglas
    literal_type: xsd:integer
    relation: :hasBirthYear
  AddTriple (13c9cdc6-f6c9-4ae7-9173-e2dc357adcef)
 Call ID: 13c9cdc6-f6c9-4ae7-9173-e2dc357adcef
  Args:
    target: :WalburgaDouglas
    relation: :isSonOf
    source: :MauritzOttoWenzelDouglas
  AddTriple (03ce47d6-141d-4191-abc2-a5046039d2ab)
 Call ID: 03ce47d6-141d-4191-abc2-a5046039d2ab
  Args:
    source: :MauritzOttoWenzelDouglas
    target: :CarlAxelArchibaldDouglas
    relation: :isSonOf
  AssignClass (733b1610-e1d6-400f-8f5e-156ec1248fd7)
 Call ID: 733b1610-e1d6-400f-8f5e-156ec1248fd7
  Args:
    type: :Man
    source: :CharlesI
  AssignClass (7c02ac17-5bcb-4eec-b7c3-0c1a4539c594)
 Call ID: 7c02ac17-5bcb-4eec-b7c3-0c1a4539c594
  Args:
    source: :CharlesI
    type: :Person
  AssignClass (b8cd51e1-f1d6-4aff-97a2-55027db839a8)
 Call ID: b8cd51e1-f1d6-4aff-97a2-55027db839a8
  Args:
    source: :CharlesI
    type: :Ancestor
  AddTriple (b6243c3f-3129-4a9f-8958-bc62086849c9)
 Call ID: b6243c3f-3129-4a9f-8958-bc62086849c9
  Args:
    target: :CharlesI
    relation: :hasAncestor
    source: :WalburgaDouglas
  Finish (d0a9c582-f2c3-4af6-9b85-b2ac7ded8181)
 Call ID: d0a9c582-f2c3-4af6-9b85-b2ac7ded8181
  Args: