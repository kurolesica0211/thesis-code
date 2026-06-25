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
Princess Hélène of Orléans (French: Princesse Hélène Louise Henriette d'Orléans; 13 June 1871 – 21 January 1951) was a member of the deposed Orléans royal family of France and, by marriage to the head of a cadet branch of the Italian royal family, the Duchess of Aosta.
Family

Hélène was the third of eight children born to Prince Philippe, Count of Paris, and Infanta Maria Isabel of Spain.
Her father was a grandson of Louis Philippe I, King of the French, and had been heir-apparent to the throne from 1842 until the exile of the dynasty in 1848.
Repatriating to France at the end of June 1871, the family took up residence in Paris at the Hotel Fould on the Rue du Faubourg Saint-Honoré, as guests of their uncle, Henri, Duke of Aumale, whose wealth and properties in France had not been confiscated in 1852, unlike those of the other Orléans princes.
On 21 December 1872 the National Assembly enacted a law of restitution, authorising restoration of approximately 40 million of the eighty million francs worth of property which had formerly belonged to the House of Orléans, although the actual re-acquisition of that wealth would take several years.
Meanwhile, a close friend of the Count and Countess of Paris, Maria Brignole Sale De Ferrari, placed at their disposal the ground floor and gardens of the Hôtel Matignon on the rue de Varenne in Paris.
Along the adjacent rue de Babylone the Duchess had a two-story town house built to accommodate the Orléans children, their governesses and tutors, which served as Hélène's home from 1876 until her father was again exiled.
In 1883 the last legitimate prince in the male-line of Louis XV, Henri, Count of Chambord, died childless leaving, in the eyes of French royalists excepting recalcitrant legitimists, the Count of Paris as heir to the Bourbon crown of France.
However, celebrations in Paris in the spring of 1886 prior to the marriage in Lisbon of Hélène's eldest sister Amélie to Carlos of Braganza-Coburg, Prince Royal of Portugal, evoked such clear expressions of monarchist support for the House of Orléans that on 22 July the French Republic took the precaution of banishing the heads of France's former ruling dynasties, the Orléans and Bonapartes, from the country.
Nearly all of the Orléans promptly left France, with Hélène and her parents going on to visit Tunbridge Wells in England and then travelling to Scotland before taking up residence in October at Sheen House in East Sheen, England.
Potential matches

Most of Hélène's siblings had married well, including Amélie, Queen of Portugal, Philippe, Duke of Orléans (who married Archduchess Maria Dorothea of Austria) and Isabelle, Duchess of Guise, and Hélène's parents had hopes that she would marry an heir to a throne.
Those hopes were fanned by the fact that Hélène was considered a great beauty for the day, and one contemporary source stated that she was "the personification of womanly health and beauty, distinguished as a graceful athlete and charming linguist".
Relationship with the Duke of Clarence

Prince Albert Victor, Duke of Clarence and Avondale ("Eddy") was the eldest son of the future Edward VII and grandson of then reigning Queen Victoria.
During the spring and summer of 1890, Eddy and Hélène were allowed to become acquainted at the homes of Clarence's sister Princess Louise, Duchess of Fife in Sheen and in Scotland, and, with the encouragement of their mothers, Hélène and Eddy fell in love.
On 29 August, Clarence obtained permission to meet alone with his grandmother at Balmoral Castle in Scotland, and brought Hélène with him.
Marriage to a Catholic would have entailed constitutional forfeiture of Eddy's claim to the British throne, pursuant to the Act of Settlement, but Hélène offered to become an Anglican.
When Queen Victoria expressed surprise at Hélène's offer, Hélène wept and insisted that her willingness to do so was for the sake of love.
This included her expectation that Hélène's father would not consent to his daughter's change of faith.
Hélène's father refused to countenance the marriage, was adamant she could not convert and informed the Queen of his decision.
He granted permission, nonetheless, for Hélène to personally beseech Pope Leo XIII for a dispensation to marry Clarence, but the Pope confirmed her father's verdict and the courtship ended.
Clarence never got over his feelings for Hélène and their relationship is commemorated at his tomb at Windsor Castle by a bead wreath with the single word "HELENE" written upon it.
Queen Victoria wrote to her grandson recommending another of her grandchildren, Princess Margaret of Prussia, as an alternative, but nothing came of that suggestion, and Clarence told his grandmother that his love for another cousin, Alix of Hesse (a match for which the Queen had long hoped) had gone unrequited.
An engagement to Princess Mary of Teck was later arranged, but Clarence died before their wedding could take place.
Although acknowledging his parents' desires for a French alliance in his diary, the future Tsar Nicholas II of Russia (a first cousin of Clarence) never pursued their choice, Hélène, as he was already in love with the aforementioned Alix of Hesse and secured their permission to marry her in 1894.
In 1892, while travelling in Egypt with her brother Philippe, Hélène met Ernst Gunther, Duke of Schleswig-Holstein, who decided that he would marry her, to the fury of his sister, the German Empress Augusta Victoria.
German diplomatic pressure put an end to Ernst Gunther's hopes, which were probably fruitless in any event as Hélène showed no interest in his advances.
In the meantime, he met his future wife, Countess Sophie Chotek, and never considered Hélène again.
Marriage and children

On 25 June 1895, at the Church of St. Raphael in Kingston upon Thames, Hélène married Prince Emanuele Filiberto of Savoy, 2nd Duke of Aosta (1869–1931).
The wedding was attended by Crown Prince Victor Emmanuel of Italy, the Prince and Princess of Wales and others of the British royal family.
The couple had two sons:


Widowed in 1931, Princess Hélène was married for a second time in 1936 to Colonel Otto Campini.
Avocations

In 1892 Hélène travelled with her brother Philippe to Egypt and Palestine, the first of many trips outside of Europe.
After the breakdown of both her health and her marriage, Hélène began frequent trips to Africa which lasted up to ten months at a time.
In 1913-1914 Hélène undertook a round-the-world trip which she recorded in another travel book.
War-time nurse

When the Italo-Turkish War broke out, Hélène trained as a nurse and went aboard the hospital ship Memfi, where she cared for wounded soldiers and those suffering from disease.
During World War I, Hélène became the head of the Italian Red Cross nurses and spent much of her time on or near the front lines.
For her service, Hélène was awarded the Italian Silver Medal for bravery, the Romanian Regina Maria Cross, the French Croix de Guerre, and the Insignia of a Dame Grand Cross of the Order of the British Empire.



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
  AssignClass (043e665c-1021-41f4-8434-82ea6087ab7d)
 Call ID: 043e665c-1021-41f4-8434-82ea6087ab7d
  Args:
    source: :HeleneOfOrleans
    type: :Person
  AssignClass (413b75f9-37a3-4ab2-9a6e-18f6f6c326eb)
 Call ID: 413b75f9-37a3-4ab2-9a6e-18f6f6c326eb
  Args:
    source: :HeleneOfOrleans
    type: :Woman
  AddLiteral (eef40d6d-4593-4035-8d52-8b7b9d1fcb02)
 Call ID: eef40d6d-4593-4035-8d52-8b7b9d1fcb02
  Args:
    literal_value: 1871
    literal_type: xsd:integer
    relation: :hasBirthYear
    source: :HeleneOfOrleans
  AddLiteral (5a3b5985-b493-43a3-ba30-eddf6765ef88)
 Call ID: 5a3b5985-b493-43a3-ba30-eddf6765ef88
  Args:
    literal_value: 1951
    relation: :hasDeathYear
    source: :HeleneOfOrleans
    literal_type: xsd:integer
  AssignClass (8f3abf8f-5589-462d-81b0-ec33c1323006)
 Call ID: 8f3abf8f-5589-462d-81b0-ec33c1323006
  Args:
    source: :PhilippeCountOfParis
    type: :Person
  AssignClass (590a00dd-428a-42e3-9f13-310c8f2c5405)
 Call ID: 590a00dd-428a-42e3-9f13-310c8f2c5405
  Args:
    source: :PhilippeCountOfParis
    type: :Man
  AssignClass (ea946e0e-e20c-45df-afda-cce35a185c50)
 Call ID: ea946e0e-e20c-45df-afda-cce35a185c50
  Args:
    source: :MariaIsabelOfSpain
    type: :Person
  AssignClass (c66218a8-3d81-4566-8260-2fc0177984a1)
 Call ID: c66218a8-3d81-4566-8260-2fc0177984a1
  Args:
    source: :MariaIsabelOfSpain
    type: :Woman
  AddTriple (461e8d82-66ca-46e8-ae0f-541d36169e1b)
 Call ID: 461e8d82-66ca-46e8-ae0f-541d36169e1b
  Args:
    target: :PhilippeCountOfParis
    source: :HeleneOfOrleans
    relation: :hasFather
  AddTriple (447e9da1-659f-47e2-8cf7-cac4c68b5c15)
 Call ID: 447e9da1-659f-47e2-8cf7-cac4c68b5c15
  Args:
    target: :MariaIsabelOfSpain
    source: :HeleneOfOrleans
    relation: :hasMother
  AssignClass (4513252e-179f-48e2-a7b3-a3c9a9fcc6c5)
 Call ID: 4513252e-179f-48e2-a7b3-a3c9a9fcc6c5
  Args:
    source: :AmelieOfOrleans
    type: :Person
  AssignClass (fc4f1c18-a087-49c0-b04d-f6462b078679)
 Call ID: fc4f1c18-a087-49c0-b04d-f6462b078679
  Args:
    source: :AmelieOfOrleans
    type: :Woman
  AddTriple (19b6a3d9-0e71-4c80-bd49-cead68f45f4e)
 Call ID: 19b6a3d9-0e71-4c80-bd49-cead68f45f4e
  Args:
    target: :AmelieOfOrleans
    source: :HeleneOfOrleans
    relation: :hasSister
  AssignClass (78beaf07-ff90-49fc-aaf9-953e12c1b4c4)
 Call ID: 78beaf07-ff90-49fc-aaf9-953e12c1b4c4
  Args:
    source: :PhilippeDukeOfOrleans
    type: :Person
  AssignClass (b8997272-6c8a-40de-b1b0-4a4223a40f3e)
 Call ID: b8997272-6c8a-40de-b1b0-4a4223a40f3e
  Args:
    source: :PhilippeDukeOfOrleans
    type: :Man
  AddTriple (b0500d55-3fbd-4239-8f34-650b3b124d39)
 Call ID: b0500d55-3fbd-4239-8f34-650b3b124d39
  Args:
    source: :HeleneOfOrleans
    relation: :hasBrother
    target: :PhilippeDukeOfOrleans
  AssignClass (838cd998-da65-45f4-a854-7df10a941139)
 Call ID: 838cd998-da65-45f4-a854-7df10a941139
  Args:
    source: :IsabelleDuchessOfGuise
    type: :Person
  AssignClass (5abd66cb-6192-4729-b9f1-3ff1a259c526)
 Call ID: 5abd66cb-6192-4729-b9f1-3ff1a259c526
  Args:
    source: :IsabelleDuchessOfGuise
    type: :Woman
  AddTriple (5b0b4a68-82a4-42bf-a70c-ae9bd23e3aa6)
 Call ID: 5b0b4a68-82a4-42bf-a70c-ae9bd23e3aa6
  Args:
    relation: :hasSister
    source: :HeleneOfOrleans
    target: :IsabelleDuchessOfGuise
  AssignClass (e2d4919b-44d5-4b38-8817-fac8acbce847)
 Call ID: e2d4919b-44d5-4b38-8817-fac8acbce847
  Args:
    source: :EmanueleFilibertoDukeOfAosta
    type: :Person
  AssignClass (8e835614-3afb-4748-98f1-b9237d45a704)
 Call ID: 8e835614-3afb-4748-98f1-b9237d45a704
  Args:
    source: :EmanueleFilibertoDukeOfAosta
    type: :Man
  AddLiteral (64e00089-b4eb-4609-9313-bfcf4eb9974b)
 Call ID: 64e00089-b4eb-4609-9313-bfcf4eb9974b
  Args:
    source: :HeleneOfOrleans
    relation: :hasMarriageYear
    literal_type: xsd:integer
    literal_value: 1895
  AssignClass (6448a3e5-aef7-4210-9c8c-6507263c7341)
 Call ID: 6448a3e5-aef7-4210-9c8c-6507263c7341
  Args:
    source: :OttoCampini
    type: :Person
  AssignClass (4810b076-2cce-421c-95d7-6d05c969b6b8)
 Call ID: 4810b076-2cce-421c-95d7-6d05c969b6b8
  Args:
    source: :OttoCampini
    type: :Man
  AddLiteral (6fdf06a6-a15b-4510-98fc-dbcd364c297d)
 Call ID: 6fdf06a6-a15b-4510-98fc-dbcd364c297d
  Args:
    relation: :hasMarriageYear
    source: :HeleneOfOrleans
    literal_type: xsd:integer
    literal_value: 1936
  Finish (d60a2161-b67e-4ab0-86d0-2338cb51f951)
 Call ID: d60a2161-b67e-4ab0-86d0-2338cb51f951
  Args: