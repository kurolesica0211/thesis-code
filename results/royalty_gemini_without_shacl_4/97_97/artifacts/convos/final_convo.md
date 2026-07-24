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
Descendants of Prince Felix and also members of the Grand Ducal Family of Luxembourg:


Princess Joan


Descendants of Prince René:


Princess Maria Pia


Princess Marina


Descendants of Prince Louis:


Prince RémyPrincess Elisabeth


Princess Chantal
Prince JeanPrincess Virginia


Princess Beatrix*


Princess Margriet*Pieter van Vollenhoven*


Princess Margarita of Bourbon-Parma, Countess of Colorno (Dutch: Margarita Maria Beatrix Prinses de Bourbon de Parme; born 13 October 1972), is the eldest daughter of Princess Irene of the Netherlands and Carlos Hugo, Duke of Parma.
She is a member of the House of Bourbon-Parma as well an extended member of the Dutch royal family.
Per a 1996 royal decree issued by Queen Beatrix, she is entitled to the style and title Her Royal Highness Princess Margarita de Bourbon de Parme in the Netherlands as a member of the extended royal family.
Early life

Born in Nijmegen, she is the twin sister of Prince Jaime.
She also has an elder brother, Prince Carlos, and a younger sister, Princess Carolina.
Her godparents are Queen Beatrix of the Netherlands (maternal aunt) and Prince Sixtus Henry of Bourbon-Parma (paternal uncle).
She is the eldest granddaughter of Queen Juliana and Prince Bernhard.
Together with her mother and her siblings she moved from Spain to The Netherlands, to live with her grandparents, Queen Juliana of the Netherlands and Prince Bernhard of Lippe-Biesterfeld at Baarn.
Margarita studied Cultural Anthropology at the Vrije Universiteit of Amsterdam and is an interior decorator.
First marriage and controversy

On 19 June 2001, Princess Margarita married the entrepreneur Edwin Karel Willem de Roy van Zuydewijn, member of a Dutch patrician family.
In 2003, a series of incidents became known as the Margarita-affair.
Margarita and her husband accused the Dutch Royal House and the Dutch secret service of obstructing the affairs of Fincentives, the company of de Roy van Zuydewijn.
The couple's home was the Bartas Castle in Saint-Georges, Gers, France, but by 2004 the princess was increasingly seen more often in Amsterdam than there.
Because of the quarrels between the princess and the Dutch Royal family during the Margarita-affair, she was not welcome at the marriage of her cousin Willem-Alexander, Prince of Orange to Máxima Zorreguieta, or at the funeral of her uncle, Prince Claus of the Netherlands.
On 20 February 2023, Princess Margarita and Ten Cate announced their divorce.
Together they have two daughters:


Margarita currently lives in Wassenaar.
Titles, styles and honours

Already a ducal princess from birth, her father bestowed on 2 September 1996 the substantive title Contessa di Colorno (Countess of Colorno) upon her.
The same year she was incorporated into the Dutch nobility by her aunt Queen Beatrix, with the highest noble title Prinses de Bourbon de Parme (Princess of Bourbon-Parma) and styled Hare Koninklijke Hoogheid (Her Royal Highness).
She does not belong to the House of Orange-Nassau or the limited Dutch royal house, but as a granddaughter of Queen Juliana, she is officially a member of the more extended Dutch royal family.
Ancestry

References

External links

2 also Princess of Lippe-Biesterfeld



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
  AssignClass (af7c600a-c8f1-4fdc-af2c-336d5e14d6fa)
 Call ID: af7c600a-c8f1-4fdc-af2c-336d5e14d6fa
  Args:
    source: :PrincessMargaritaOfBourbonParma
    type: :Woman
  AssignClass (4817b3e1-cbab-4e85-a869-6f73d3136d03)
 Call ID: 4817b3e1-cbab-4e85-a869-6f73d3136d03
  Args:
    type: :Woman
    source: :PrincessIreneOfTheNetherlands
  AssignClass (438b9ebc-c5db-419f-99a3-cb17790fe020)
 Call ID: 438b9ebc-c5db-419f-99a3-cb17790fe020
  Args:
    type: :Man
    source: :CarlosHugoDukeOfParma
  AddTriple (971b1848-155f-4450-acba-19dd5d884daa)
 Call ID: 971b1848-155f-4450-acba-19dd5d884daa
  Args:
    relation: :hasMother
    target: :PrincessIreneOfTheNetherlands
    source: :PrincessMargaritaOfBourbonParma
  AddTriple (96eacfe0-f100-4c72-b55b-b35d198f1569)
 Call ID: 96eacfe0-f100-4c72-b55b-b35d198f1569
  Args:
    source: :PrincessMargaritaOfBourbonParma
    relation: :hasFather
    target: :CarlosHugoDukeOfParma
  AssignClass (8fdf5d75-a459-4b72-8336-81b3ab24ba3d)
 Call ID: 8fdf5d75-a459-4b72-8336-81b3ab24ba3d
  Args:
    type: :Man
    source: :PrinceJaime
  AssignClass (63141fdc-c42d-469d-a72c-2c07dc137108)
 Call ID: 63141fdc-c42d-469d-a72c-2c07dc137108
  Args:
    source: :PrinceCarlos
    type: :Man
  AssignClass (da5d803e-2f00-4ca2-8a93-41cf0a142390)
 Call ID: da5d803e-2f00-4ca2-8a93-41cf0a142390
  Args:
    type: :Woman
    source: :PrincessCarolina
  AddTriple (a31667c5-7ba5-45d0-9381-1a67c2dc429b)
 Call ID: a31667c5-7ba5-45d0-9381-1a67c2dc429b
  Args:
    target: :PrinceJaime
    relation: :isSiblingOf
    source: :PrincessMargaritaOfBourbonParma
  AddTriple (77927031-4732-42fe-9d51-4f16af6f5626)
 Call ID: 77927031-4732-42fe-9d51-4f16af6f5626
  Args:
    source: :PrincessMargaritaOfBourbonParma
    relation: :isSiblingOf
    target: :PrinceCarlos
  AddTriple (70fc2d20-d6e1-4b80-9959-b0eb0462a44d)
 Call ID: 70fc2d20-d6e1-4b80-9959-b0eb0462a44d
  Args:
    target: :PrincessCarolina
    relation: :isSiblingOf
    source: :PrincessMargaritaOfBourbonParma
  AssignClass (8891c5c0-a5f4-442e-aeb1-e819d86b314c)
 Call ID: 8891c5c0-a5f4-442e-aeb1-e819d86b314c
  Args:
    type: :Woman
    source: :QueenJuliana
  AssignClass (25afd77a-5a38-42cf-aa1c-9e723277c4e3)
 Call ID: 25afd77a-5a38-42cf-aa1c-9e723277c4e3
  Args:
    type: :Man
    source: :PrinceBernhard
  AddTriple (c7916995-dd2f-4fe3-a512-44d417a2b591)
 Call ID: c7916995-dd2f-4fe3-a512-44d417a2b591
  Args:
    source: :PrincessIreneOfTheNetherlands
    target: :QueenJuliana
    relation: :hasMother
  AddTriple (a128f043-7dc2-4c8d-93f3-7f35013d5e1c)
 Call ID: a128f043-7dc2-4c8d-93f3-7f35013d5e1c
  Args:
    target: :PrinceBernhard
    relation: :hasFather
    source: :PrincessIreneOfTheNetherlands
  AssignClass (58be7447-4b71-4a61-be61-b2b2283d54e6)
 Call ID: 58be7447-4b71-4a61-be61-b2b2283d54e6
  Args:
    source: :EdwinKarelWillemDeRoyVanZuydewijn
    type: :Man
  AddTriple (9643374b-2e78-4611-8944-7382553452ce)
 Call ID: 9643374b-2e78-4611-8944-7382553452ce
  Args:
    target: :EdwinKarelWillemDeRoyVanZuydewijn
    relation: :hasRelation
    source: :PrincessMargaritaOfBourbonParma
  AssignClass (29b29259-9f02-40ff-8d1f-338dd2980edd)
 Call ID: 29b29259-9f02-40ff-8d1f-338dd2980edd
  Args:
    source: :QueenBeatrix
    type: :Woman
  AddTriple (3e265964-4f71-419c-804e-b41daa403656)
 Call ID: 3e265964-4f71-419c-804e-b41daa403656
  Args:
    relation: :isSisterOf
    target: :PrincessIreneOfTheNetherlands
    source: :QueenBeatrix
  AssignClass (53dc74b6-35e0-4eff-a0fc-570e82ef759e)
 Call ID: 53dc74b6-35e0-4eff-a0fc-570e82ef759e
  Args:
    type: :Man
    source: :PrinceSixtusHenryOfBourbonParma
  AddTriple (19d061da-4573-40f9-82b2-0eff2fdc6efc)
 Call ID: 19d061da-4573-40f9-82b2-0eff2fdc6efc
  Args:
    source: :PrinceSixtusHenryOfBourbonParma
    relation: :isBrotherOf
    target: :CarlosHugoDukeOfParma
  Finish (fdfbcd26-1be9-485c-afe2-560c73a8beb8)
 Call ID: fdfbcd26-1be9-485c-afe2-560c73a8beb8
  Args: